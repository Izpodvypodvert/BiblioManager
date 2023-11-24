import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from books.models import Book


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_book():
    return Book.objects.create(title='Тестовая книга', author='Автор', publication_year=2020, ISBN='123-456')


@pytest.mark.django_db
def test_get_book_list(api_client):
    """Проверкa получения книг."""
    url = reverse('api:book-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK  # type: ignore


@pytest.mark.django_db
def test_create_book(api_client):
    """Проверкa создания книги."""
    url = reverse('api:book-list')
    book_data = {'title': 'Новая книга', 'author': 'Автор',
                 'publication_year': 2020, 'ISBN': '123-456'}
    response = api_client.post(url, book_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED  # type: ignore


@pytest.mark.django_db
def test_update_book(api_client, create_book):
    """Проверка обновленния книги."""
    book_id = create_book.id
    url = reverse('api:book-detail', kwargs={'pk': book_id})
    updated_data = {'title': 'Обновленное название'}
    response = api_client.patch(url, updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK  # type: ignore


@pytest.mark.django_db
def test_delete_book(api_client, create_book):
    """Проверка удаления книги."""
    book_id = create_book.id
    url = reverse('api:book-detail', kwargs={'pk': book_id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT  # type: ignore
