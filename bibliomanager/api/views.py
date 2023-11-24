from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from books.models import Book
from .serializers import BookSerializer, UserRegistrationSerializer
from .tasks import send_welcome_email


class BookViewSet(ModelViewSet):
    """
    Представление для просмотра, редактирования, поиска и фильтрации книг.

    Это представление позволяет получить список всех книг, создать новую книгу,
    получить детали конкретной книги, обновить или удалить книгу. Поддерживает
    поиск по названию и автору книг, а также фильтрацию по автору, году издания и ISBN.

    Фильтрация осуществляется через параметры запроса, например:
    `/books/?author=Толстой` для фильтрации по автору или
    `/books/?search=Война и мир` для поиска по названию.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author', 'publication_year', 'ISBN']
    search_fields = ['title', 'author']


class UserRegistrationView(CreateAPIView):
    """
    Представление для регистрации нового пользователя.

    При успешной регистрации отправляет пользователю приветственное письмо.
    """
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_welcome_email.delay(user.email)
