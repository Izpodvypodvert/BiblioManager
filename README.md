# BiblioManager

BiblioManager - это веб-приложение для управления книгами в библиотеке. Оно позволяет пользователям просматривать, добавлять, обновлять и удалять информацию о книгах, включая название, автора, год издания и ISBN.

## Особенности:

-   Получение списка всех книг.
-   Получение информации о конкретной книге.
-   Создание новой книги.
-   Обновление информации о книге.
-   Удаление книги.
-   Асинхронная задача, которая отправляет приветственное электронное письмо пользователю при его регистрации.

## Технологии

-   Backend: **Django**, **Django REST Framework**
-   Database: **MySQL**
-   Дополнительные инструменты: **Docker**, **Redis**, **Celery**

## Установка и Запуск

### Предварительные требования

-   Python 3.10+
-   pip и virtualenv
-   Docker
-   Docker Compose

### Установка

1. Клонируйте репозиторий:

```sh
    git clone git@github.com:Izpodvypodvert/BiblioManager.git
```

2. Создайте и активируйте виртуальное окружение:

```sh
    python3.10 -m venv venv
    source venv/bin/activate
    или
    source venv/Scripts/activate на windows
```

3. Установите зависимости:

```sh
pip install -r requirements.txt
```

4. Запустите сервер разработки:

```sh
python manage.py runserver
```

5. Перейдите по адресу http://localhost:8000 в вашем браузере.

### Docker

Чтобы запустить приложение в Docker, используйте:

```sh
docker-compose up
```

## Документация API

### Обзор

Интегрирован `drf-yasg` для автоматической генерации документации Swagger и ReDoc для REST API. Это позволяет легко просматривать и тестировать все доступные эндпоинты API.

### Доступ к документации

Документация доступна в двух форматах:

1. **Swagger UI:**

    - Доступен по адресу: [http://localhost:8000/api/swagger/](http://localhost:8000/api/swagger/)
    - Интерактивный интерфейс для просмотра и тестирования эндпоинтов API.

2. **ReDoc:**
    - Доступен по адресу: [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)
    - Альтернативное представление документации с улучшенной структурой и читаемостью.
