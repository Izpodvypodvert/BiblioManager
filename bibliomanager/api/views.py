from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from books.models import Book, BookLoan
from .permissions import IsAdminOrReadOnly
from .serializers import BookLoanSerializer, BookSerializer, UserBookLoanSerializer, UserRegistrationSerializer
from .tasks import send_welcome_email


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description=(
        """
        Представление для просмотра, редактирования, поиска и фильтрации книг.
        
        Доступно для чтения всем пользователям, но создание, обновление и удаление
        книг разрешено только администраторам.
        
        `/books/?author=Уильям Шоттс` для фильтрации по автору или
        `/books/?search=Компьютерные сети` для поиска по названию.
        """)
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
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """
        Переопределяет базовый queryset. Для администраторов возвращает все книги.
        Для остальных пользователей возвращает только книги, которые в данный момент
        не забронированы.
        """
        user = self.request.user
        if user.is_staff or user.is_superuser:  # type: ignore
            return Book.objects.all()

        return Book.objects.filter(borrowed_by__isnull=True)


class UserRegistrationView(CreateAPIView):
    """
    Представление для регистрации нового пользователя.

    При успешной регистрации отправляет пользователю приветственное письмо.
    """
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_welcome_email.delay(user.email)


class BorrowBookView(APIView):
    """
    Представление для обработки запросов на взятие книги пользователями.

    Этот класс обрабатывает POST-запросы, в которых пользователи могут указать
    книгу, которую они хотят взять. Если выбранная книга доступна, запрос
    обновляет статус книги и регистрирует заимствование в базе данных.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        if BookLoan.objects.filter(user=request.user, actual_borrowed_date__isnull=True).count() >= settings.MAX_BOOKS_PER_USER:
            return Response({'message': 'Вы не можете взять более двух книг'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book = Book.objects.get(id=book_id)
            if book.borrowed_by is not None:
                return Response({'message': 'Эта книга уже взята'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = BookLoanSerializer(
                data={
                    'book': book.id,  # type: ignore
                }
            )
            if serializer.is_valid():
                book_loan = serializer.save(user=request.user)
                book.borrowed_by = request.user
                book.save()
                return Response({'message': 'Книга успешно взята'}, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Book.DoesNotExist:
            return Response({'message': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)


class ReturnBookView(APIView):
    """
    Представление для обработки запросов на возврат книги пользователями.

    Пользователи могут отправить DELETE-запрос для возврата книги, которую они ранее
    забронировали, но физически еще не забрали (actual_borrowed_date == null).
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, book_id):
        try:
            book_loan = BookLoan.objects.get(
                book_id=book_id, user=request.user)

            if book_loan.actual_borrowed_date is not None:
                return Response({'message': 'Книга уже была фактически забрана'}, status=status.HTTP_400_BAD_REQUEST)

            book_loan.delete()
            book = Book.objects.get(id=book_id)
            book.borrowed_by = None
            book.save()

            return Response({'message': 'Книга успешно возвращена'}, status=status.HTTP_200_OK)

        except BookLoan.DoesNotExist:
            return Response({'message': 'Заимствование книги не найдено'}, status=status.HTTP_404_NOT_FOUND)
        except Book.DoesNotExist:
            return Response({'message': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)


class UserBookLoansView(APIView):
    """
    API view для получения списка взятых или зарезервированных книг текущим пользователем.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_book_loans = BookLoan.objects.filter(user=request.user)
        serializer = UserBookLoanSerializer(user_book_loans, many=True)
        return Response(serializer.data)


class MeView(APIView):
    """
    API view для получения информации о текущем пользователе.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        })
