from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from books.models import Book
from .serializers import BookSerializer, UserRegistrationSerializer
from .tasks import send_welcome_email


class BookViewSet(ModelViewSet):
    """
    Представление для просмотра и редактирования книг.

    Это представление позволяет получить список всех книг, создать новую книгу,
    получить детали конкретной книги, обновить или удалить книгу.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class UserRegistrationView(CreateAPIView):
    """
    Представление для регистрации нового пользователя.

    При успешной регистрации отправляет пользователю приветственное письмо.
    """
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_welcome_email.delay(user.email)
