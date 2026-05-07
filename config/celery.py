import os
from celery import Celery

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Загружаем настройки из Django settings, используя префикс CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим задачи в приложениях Django (tasks.py)
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')