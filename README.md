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

-   Docker
-   Docker Compose

### Установка

1. Клонируйте репозиторий:

```sh
    git clone git@github.com:Izpodvypodvert/BiblioManager.git
```

2. Перед запуском приложения, создайте файл `.env` в корневой директории проекта:

```env
SECRET_KEY=django-insecure-nv)q55+n=o^4*%9xb1m7^oje#b^-5^u#ju9g^_nw)azi1nnmm$
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

REDIS_URL=redis://redis:6379

MYSQL_DATABASE=mydb
MYSQL_USER=myuser
MYSQL_PASSWORD=secret_password
MYSQL_ROOT_PASSWORD=super_secret_password
DB_HOST=db
DB_PORT=3306

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=hxsf cmtn rnbn wwww
```

#### [->Как настроить SMTP Server<-](https://www.youtube.com/watch?v=HFTesr_r_WI)

3. Чтобы запустить приложение в Docker, используйте:

```sh
docker-compose up -d
```

4. Перейдите по адресу http://localhost:8000/api/swagger/ в вашем браузере.

5. Чтобы остановить и удалить созданные контейнеры, используйте команду:

```sh
docker-compose down
```

### Запуск тестов с использованием Docker

Чтобы запустить тесты в Docker, используйте:

```sh
docker-compose run web pytest
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
