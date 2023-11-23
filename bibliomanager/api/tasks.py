from celery import shared_task
from django.core.mail import send_mail
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
