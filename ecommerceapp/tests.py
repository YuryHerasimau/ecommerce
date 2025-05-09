from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Network, Product


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