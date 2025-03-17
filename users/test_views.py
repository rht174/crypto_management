from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from organizations.models import Organization

User = get_user_model()


class UserAPITests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email': 'test@example.com'
        }

    def test_user_registration(self):
        url = reverse('user-register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_user_login(self):
        # Create user first
        User.objects.create_user(**self.user_data)

        # Try to obtain token
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_add_user_to_organization(self):
        # Create user and org
        user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)

        org = Organization.objects.create(
            name='Test Org',
            owner=user
        )

        # Test adding organization to user
        url = reverse('user-detail', kwargs={'pk': user.id})
        response = self.client.patch(url, {
            'organization_ids': [str(org.id)]
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(org, user.organizations.all())

    def test_invalid_registration(self):
        url = reverse('user-register')
        # Try to register without required fields
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_username(self):
        # Create first user
        User.objects.create_user(**self.user_data)

        # Try to create another user with same username
        url = reverse('user-register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
