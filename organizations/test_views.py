from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Organization

User = get_user_model()


class OrganizationAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.org_data = {'name': 'Test Organization'}

    def test_create_organization(self):
        url = reverse('organization-list')
        response = self.client.post(url, self.org_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organization.objects.count(), 1)
        org = Organization.objects.first()
        self.assertEqual(org.name, 'Test Organization')
        self.assertEqual(org.owner, self.user)
        self.assertIn(org, self.user.organizations.all())

    def test_list_organizations(self):
        org = Organization.objects.create(name='Test Org', owner=self.user)
        self.user.organizations.add(org)
        url = reverse('organization-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthorized_access(self):
        self.client.force_authenticate(user=None)
        url = reverse('organization-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization(self):
        org = Organization.objects.create(name='Test Org', owner=self.user)
        self.user.organizations.add(org)
        url = reverse('organization-detail', kwargs={'pk': org.id})
        data = {'name': 'Updated Org Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Organization.objects.get(
            id=org.id).name, 'Updated Org Name')

    def test_delete_organization(self):
        org = Organization.objects.create(name='Test Org', owner=self.user)
        self.user.organizations.add(org)
        url = reverse('organization-detail', kwargs={'pk': org.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Organization.objects.count(), 0)

    def test_non_owner_update_organization(self):
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        org = Organization.objects.create(name='Test Org', owner=other_user)
        url = reverse('organization-detail', kwargs={'pk': org.id})
        data = {'name': 'Updated Org Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
