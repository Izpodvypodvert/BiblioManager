from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    '''
    Пользовательская модель, расширяющая стандартную модель пользователя Django.
    Исключает стандартные поля 'first_name' и 'last_name'.
    Наследует поля 
    'username' - Имя пользователя,
    'date_joined' - Дата регистрации.
    '''
    first_name = None
    last_name = None
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=35,
        error_messages={
            'unique': (
                'Пользователь с такой почтой уже '
                'существует.'),
        }
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}: {self.email}'
