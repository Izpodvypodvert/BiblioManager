import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bibliomanager.settings')

app = Celery('bibliomanager')
app.conf.broker_connection_retry_on_startup = True
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'Удаление записей резерва книг пользователями каждый час': {
        'task': 'api.tasks.delete_unclaimed_book_loans',
        'schedule': crontab(minute='0'),
    },
}

app.autodiscover_tasks()
