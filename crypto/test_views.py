from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from organizations.models import Organization
from .models import CryptoPrice
from decimal import Decimal
from django.utils import timezone

User = get_user_model()


class CryptoPriceAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.org = Organization.objects.create(
            name='Test Org',
            owner=self.user
        )
        self.user.organizations.add(self.org)
        self.client.force_authenticate(user=self.user)
        self.current_time = timezone.now()

    def test_list_crypto_prices(self):
        CryptoPrice.objects.create(
            org_id=self.org,
            symbol='BTC',
            price=Decimal('45000.00'),
            timestamp=self.current_time
        )
        url = reverse('cryptoprice-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(str(self.org.id), response.data)
        self.assertEqual(len(response.data[str(self.org.id)]['prices']), 1)

    def test_create_crypto_price(self):
        url = reverse('cryptoprice-list')
        data = {
            'symbol': 'ETH',
            'price': '3000.00',
            'org_id': str(self.org.id)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CryptoPrice.objects.count(), 1)
        self.assertEqual(CryptoPrice.objects.first().symbol, 'ETH')

    def test_unauthorized_access(self):
        self.client.force_authenticate(user=None)
        url = reverse('cryptoprice-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wrong_organization_access(self):
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        other_org = Organization.objects.create(
            name='Other Org',
            owner=other_user
        )
        data = {
            'symbol': 'ETH',
            'price': '3000.00',
            'org_id': str(other_org.id),
            'timestamp': self.current_time
        }
        url = reverse('cryptoprice-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(CryptoPrice.objects.count(), 0)

    def test_authenticated_user_can_only_get(self):
        # Create another user who isn't org owner
        other_user = User.objects.create_user(
            username='member',
            password='testpass123'
        )
        other_user.organizations.add(self.org)

        self.client.force_authenticate(user=other_user)

        # Try to create price
        url = reverse('cryptoprice-list')
        data = {
            'symbol': 'ETH',
            'price': '3000.00',
            'org_id': str(self.org.id),
            'timestamp': self.current_time
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Verify GET still works
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
