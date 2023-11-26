from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from books.models import BookLoan
from bibliomanager.settings import EMAIL_HOST_USER


@shared_task
def send_welcome_email(user_email):
    """
    Отправляет приветственное письмо на указанный адрес электронной почты.

    Эта задача используется для асинхронной отправки приветственного письма новым пользователям
    при регистрации в сервисе. Она устанавливается как задача Celery и выполняется в фоновом режиме.

    Args:
        user_email (str): Адрес электронной почты пользователя, которому будет отправлено письмо.

    Отправляет сообщение с заголовком "Добро пожаловать в наш сервис!" и телом письма "Спасибо за регистрацию.".
    """
    send_mail(
        'Добро пожаловать в наш сервис!',
        'Спасибо за регистрацию.',
        EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )


@shared_task
def delete_unclaimed_book_loans():
    """
    Celery задача для удаления невостребованных записей о заимствовании книг.

    Эта задача удаляет все записи о заимствовании книг, которые не были фактически
    взяты (actual_borrowed_date is null) в течение заданного времени после
    бронирования (определяется через TIME_TO_PICK_UP_BOOK_FROM_LIB в settings).
    Помогает поддерживать актуальность данных о доступности книг в библиотеке.
    """
    threshold_time = timezone.now() - timedelta(hours=settings.TIME_TO_PICK_UP_BOOK_FROM_LIB)
    unclaimed_loans = BookLoan.objects.filter(
        actual_borrowed_date__isnull=True,
        borrowed_date__lte=threshold_time
    )
    unclaimed_loans.delete()
