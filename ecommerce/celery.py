from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

# Создаем экземпляр Celery
app = Celery('ecommerce')

# Загружаем конфигурацию из settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим и регистрируем задачи в приложениях Django
app.autodiscover_tasks()

# Настройка расписания
app.conf.beat_schedule = {
    'increase-debt-every-3-hours': {
        'task': 'ecommerceapp.tasks.increase_debt',
        'schedule': 3 * 60 * 60,  # Каждые 3 часа
        # 'schedule': 60.0,  # Тест: каждую минуту
    },
    'decrease-debt-daily': {
        'task': 'ecommerceapp.tasks.decrease_debt',
        'schedule': crontab(hour=6, minute=30),  # Ежедневно в 6:30
        # 'schedule': 120.0,  # Тест: каждые 2 минуты
    },
}