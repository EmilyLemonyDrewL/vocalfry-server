from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from vocalfryapi.models import User

class TestUsers(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            uid="12345",
            first_name="Test",
            last_name="Test",
            user_type=0
        )
        self.url = reverse('user-list')

    def test_retrieve_user(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.user.first_name)

    def test_list_users(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], self.user.first_name)

    def test_create_user(self):
        data = {
          'uid': '54321',
          'first_name': 'Mr. Test',
          'last_name': 'Tested',
          'user_type': 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data['first_name'], 'Mr. Test')

    def test_update_user(self):
        url = reverse('user-detail', args=[self.user.id])
        data = {
          'uid': '12345',
          'first_name': 'Testing',
          'last_name': 'Testing',
          'user_type': 1
        }
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Testing')

    def test_delete_user(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
