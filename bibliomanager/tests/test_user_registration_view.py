import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_user_registration(api_client):
    """
    Тестирование регистрации нового пользователя через API.
    Тест также проверяет, что при успешной регистрации вызывается задача отправки письма с приветствием.
    """
    url = reverse('api:user-register')
    user_data = {
        'username': 'newuser',
        'password': 'password123',
        'email': 'newuser@example.com'
    }

    with patch('api.tasks.send_welcome_email.delay') as mock_send_email:
        response = api_client.post(url, user_data, format='json')

        mock_send_email.assert_called_once_with('newuser@example.com')
        assert response.status_code == 201
