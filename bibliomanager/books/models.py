from datetime import timedelta
from django.db import models
from django.conf import settings


class Book(models.Model):
    title = models.CharField('Название', max_length=200)
    author = models.CharField('Автор', max_length=100)
    publication_year = models.IntegerField('Год издания')
    ISBN = models.CharField(
        'Международный стандартный книжный номер',
        max_length=20
    )
    borrowed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='borrowed_books',
        verbose_name='Пользователь, взявший книгу'
    )

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title


class BookLoan(models.Model):
    """
    Модель заимствования книги, представляющая информацию о взятых пользователями книгах.

    При создании нового объекта автоматически устанавливается
    дата взятия (`borrowed_date`) и рассчитывается предполагаемая дата возврата (`return_date`),
    которая по умолчанию на две недели позже даты взятия.
    (`actual_borrowed_date`) - это фактическая дата взятия книги в библиотеке, которую выставляет администратор.
    Если проходит 24 часа с момента (`borrowed_date`) и клиент не забирает книгу celery удаляет запись и
    книга снова становиться доступной для других пользователей.
    """
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        verbose_name='Книга'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    borrowed_date = models.DateField('Дата резервирования', auto_now_add=True)
    actual_borrowed_date = models.DateTimeField(
        'Фактическая дата взятия книги в библиотеке',
        null=True,
        blank=True
    )
    return_date = models.DateField('Дата возврата', null=True, blank=True)

    class Meta:
        verbose_name = 'Заимствование книги'
        verbose_name_plural = 'Заимствования книг'

    def save(self, *args, **kwargs):
        new_obj_creating = not self.id  # type: ignore
        super().save(*args, **kwargs)
        if new_obj_creating and not self.return_date:
            self.return_date = self.borrowed_date + timedelta(weeks=2)
            super().save(update_fields=['return_date'])

    def __str__(self):
        return f'{self.user} взял книгу {self.book} до {self.return_date}'
