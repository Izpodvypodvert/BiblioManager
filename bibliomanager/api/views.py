from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from books.models import Book
from .serializers import BookSerializer, UserRegistrationSerializer
from .tasks import send_welcome_email


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description=(
        """Получить полный список книг.
        Можно использовать параметры фильтрации для полей 'author', 'publication_year', 'ISBN'.
        Можно производить поиск используя поля 'title', 'author', 'ISBN'
        например:
        `/books/?author=Уильям Шоттс` для фильтрации по автору или
        `/books/?search=Компьютерные сети` для поиска по названию.""")
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Создать новую книгу."
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="Получить детали конкретной книги по ID."
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Обновить книгу."
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Удалить книгу."
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description="Частично обновить информацию о книге."
))
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
    search_fields = ['title', 'author', 'ISBN']


class UserRegistrationView(CreateAPIView):
    """
    Представление для регистрации нового пользователя.

    При успешной регистрации отправляет пользователю приветственное письмо.
    """
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_welcome_email.delay(user.email)
