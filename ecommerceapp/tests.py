from django.test import TestCase


class NetworkTests(TestCase):

    def test_network_status_code(self):
        response = self.client.get('/api/network/')
        self.assertEqual(response.status_code, 403, "Should be 403 coz permissions.IsAuthenticated")