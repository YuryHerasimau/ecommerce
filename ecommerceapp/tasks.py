from celery import shared_task
from django.db import transaction
from .models import Network
import random
from datetime import datetime
from decimal import Decimal


@shared_task
def increase_debt():
    """Увеличивает задолженность на случайное число от 5 до 500 для каждой сети"""
    with transaction.atomic():
        # Блокируем выбранные записи для обновления (SELECT FOR UPDATE)
        # и загружаем ВСЕ объекты Network
        networks = Network.objects.select_for_update().all()

        for network in networks:
            # Генерируем уникальное значение для каждой сети
            amount = Decimal(str(round(random.uniform(5, 500), 2)))
            network.debt += amount
            network.save(update_fields=['debt'])
            print(f"[{datetime.now()}] Network {network.id}: debt + {amount} = {network.debt:.2f}")
    
    return f"Increased debt by {amount:.2f} for {networks.count()} networks at {datetime.now()}"


@shared_task
def decrease_debt():
    """Уменьшает задолженность на случайное число от 100 до 10000 для каждой сети"""
    with transaction.atomic():
        # Блокируем ТОЛЬКО объекты с долгом > 0 (оптимизация)
        networks = Network.objects.select_for_update().filter(debt__gt=0)
        
        for network in networks:
            # Генерируем уникальное значение для каждой сети
            amount = Decimal(str(round(random.uniform(100, 10000), 2)))
            new_debt = max(Decimal('0'), network.debt - amount) # Не уходим в минус
            print(f"[{datetime.now()}] Network {network.id}: debt - {amount} = {new_debt:.2f}")
            network.debt = new_debt
            network.save(update_fields=['debt'])
    
    return f"Decreased debt by {amount:.2f} for {networks.count()} networks at {datetime.now()}"


@shared_task
def async_clear_debt(network_ids):
    """Асинхронная очистка задолженности для >20 объектов"""
    with transaction.atomic():
        # Массовое обновление БЕЗ загрузки объектов в память
        # Прямой SQL UPDATE для всех указанных ID
        Network.objects.filter(id__in=network_ids).update(debt=0)
    
    return f"Cleared debt for {len(network_ids)} networks at {datetime.now()}"