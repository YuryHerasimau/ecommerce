from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from ecommerceapp.tasks import increase_debt, decrease_debt, async_clear_debt
from .models import Network, Product
from unittest.mock import patch


class NetworkTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            is_active=True
        )
        
        # Создаем тестовые данные
        self.product = Product.objects.create(
            name='Test Product',
            model='Model X',
            release_date='2023-01-01'
        )
        self.network = Network.objects.create(
            name='Test Network',
            level=0
        )

    def test_unauthenticated_access(self):
        response = self.client.get('/api/networks/')
        self.assertEqual(response.status_code, 403)
        
    def test_network_creation(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'New Network',
            'level': 1,
            'products': [self.product.id]
        }
        response = self.client.post('/api/networks/', data)
        self.assertEqual(response.status_code, 201)
        
    def test_product_deletion(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)


class PermissionTests(TestCase):
    def test_inactive_user_access(self):
        user = User.objects.create_user(
            username='inactive',
            password='testpass',
            is_active=False
        )
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get('/api/networks/')
        self.assertEqual(response.status_code, 403)


class CeleryTasksTests(TestCase):
    # def test_debt_increase(self):
    #     Network.objects.create(name="Test", debt=100)
        
    #     result = increase_debt.delay()
    #     self.assertTrue(result.successful())
    #     self.assertGreater(Network.objects.first().debt, 100)

    def setUp(self):
        # Создаём тестовые данные
        self.network1 = Network.objects.create(name="Network 1", debt=100)
        self.network2 = Network.objects.create(name="Network 2", debt=0)
    
    def test_increase_debt(self):
        """Тестируем увеличение долга"""
        initial_debt = self.network1.debt
        
        # Запускаем задачу синхронно для тестов
        result = increase_debt.apply()
        
        self.assertTrue(result.successful())
        self.network1.refresh_from_db()
        self.assertGreater(self.network1.debt, initial_debt)
        self.assertEqual(self.network2.debt, 0)  # Долг нулевого не должен измениться
    
    @patch('random.uniform', return_value=150.0)
    def test_increase_debt_with_mock(self, mock_uniform):
        """Тест с моком для random.uniform"""
        result = increase_debt.apply()
        
        self.assertTrue(result.successful())
        self.network1.refresh_from_db()
        self.assertEqual(self.network1.debt, 250.0)  # 100 + 150
    
    def test_decrease_debt(self):
        """Тестируем уменьшение долга"""
        self.network1.debt = 200
        self.network1.save()
        
        result = decrease_debt.apply()
        
        self.assertTrue(result.successful())
        self.network1.refresh_from_db()
        self.assertLess(self.network1.debt, 200)
        self.assertEqual(self.network2.debt, 0)  # Не должен измениться
    
    def test_decrease_debt_below_zero(self):
        """Проверяем, что долг не уходит в минус"""
        self.network1.debt = 50
        self.network1.save()
        
        with patch('random.uniform', return_value=100.0):
            decrease_debt.apply()
            
        self.network1.refresh_from_db()
        self.assertEqual(self.network1.debt, 0)
    
    def test_async_clear_debt_large_queryset(self):
        """Тестируем асинхронную очистку для >20 объектов"""
        # Создаем 21 объект для срабатывания async логики
        networks = []
        for i in range(21):
            network = Network.objects.create(
                name=f"Test Network {i}",
                debt=100 + i
            )
            networks.append(network)
        
        network_ids = [n.id for n in networks]
        
        # Мокаем Celery task чтобы проверить его вызов
        with patch('ecommerceapp.tasks.async_clear_debt.delay') as mock_async:
            # Имитируем вызов из админки
            from django.contrib.admin.sites import AdminSite
            from django.contrib import messages
            from django.http import HttpRequest
            
            class MockRequest(HttpRequest):
                def __init__(self):
                    super().__init__()
                    self._messages = messages.storage.default_storage(self)
            
            request = MockRequest()
            queryset = Network.objects.filter(id__in=network_ids)
            
            # Вызываем admin action
            from ecommerceapp.admin import clear_debt
            clear_debt(None, request, queryset)
            
            # Проверяем что async task был вызван
            mock_async.assert_called_once_with(network_ids)
            
            # Проверяем сообщение пользователю
            storage = request._messages
            messages = list(storage)
            self.assertIn("Запущена фоновая очистка", str(messages[0]))

    def test_sync_clear_debt_small_queryset(self):
        """Тестируем синхронную очистку для <=20 объектов"""
        # Создаем 5 тестовых объектов
        networks = []
        for i in range(5):
            network = Network.objects.create(
                name=f"Test Network {i}",
                debt=100 + i
            )
            networks.append(network)
        
        network_ids = [n.id for n in networks]
        queryset = Network.objects.filter(id__in=network_ids)
        
        # Вызываем admin action
        from ecommerceapp.admin import clear_debt
        clear_debt(None, None, queryset)  # request не нужен для проверки update
        
        # Проверяем что долги обнулились
        for network in networks:
            network.refresh_from_db()
            self.assertEqual(network.debt, 0)