from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from vocalfryapi.models import User

class UserTests(APITestCase):

    def new_user_for_test(self):
        self.user = User.objects.create(
            uid="12345",
            first_name="Test",
            last_name="Test",
            user_type=0
        )
        self.url = reverse('user-list')

    def retrieve_user_test(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.user.frist_name)

    def list_users_test(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], self.user.first_name)

    def create_user_test(self):
        data = {
          'uid': '54321',
          'first_name': 'Mr. Test',
          'last_name': 'Tested',
          'user-type': 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data['first_name'], 'Mr. Test')

    def update_user_test(self):
        url = reverse('user-detail', args=[self.user.id])
        data = {
          'uid': '12345',
          'first_name': 'Testing',
          'last_name': 'Testing',
          'user-type': 0
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Testing')

    def delete_user_test(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
