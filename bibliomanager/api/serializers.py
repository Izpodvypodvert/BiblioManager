from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from books.models import Book


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
