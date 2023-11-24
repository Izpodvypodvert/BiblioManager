from django.db import models


class Book(models.Model):
    title = models.CharField('Название', max_length=200)
    author = models.CharField('Автор', max_length=100)
    publication_year = models.IntegerField('Год издания')
    ISBN = models.CharField(
        'Международный стандартный книжный номер',
        max_length=20
    )

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title
