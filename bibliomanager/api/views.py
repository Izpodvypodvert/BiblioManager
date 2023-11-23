from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from books.models import Book
from .serializers import BookSerializer, UserRegistrationSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
