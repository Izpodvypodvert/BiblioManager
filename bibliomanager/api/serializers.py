from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from books.models import Book, BookLoan


User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_year', 'ISBN']

    def validate_publication_year(self, value):
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Год издания не может быть больше текущего года {current_year}.")
        if value <= 0:
            raise serializers.ValidationError(
                "Год издания должен быть больше нуля.")
        return value


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class BookLoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLoan
        fields = ['book', 'user', 'borrowed_date', 'return_date']
        read_only_fields = ['user', 'borrowed_date']

    def create(self, validated_data):
        return BookLoan.objects.create(**validated_data)


class UserBookLoanSerializer(serializers.ModelSerializer):
    book_id = serializers.ReadOnlyField(source='book.id')
    book_title = serializers.ReadOnlyField(source='book.title')
    book_author = serializers.ReadOnlyField(source='book.author')
    is_picked_up = serializers.SerializerMethodField()

    class Meta:
        model = BookLoan
        fields = ['book_id', 'book_title', 'book_author',
                  'borrowed_date', 'return_date', 'is_picked_up']

    def get_is_picked_up(self, obj):
        return obj.actual_borrowed_date is not None
