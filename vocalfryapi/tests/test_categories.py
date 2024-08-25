from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from vocalfryapi.models import Category

class TestCategories(TestCase):

    def setUp(self):
        self.category = Category.objects.create(label="Test Category")
        self.url = reverse('category-list')

    def test_retrieve_category(self):
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], "Test Category")

    def test_list_categories(self):
        Category.objects.create(label="Another Category")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_category(self):
        data = {'label': 'New Category'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['label'], 'New Category')

    def test_update_category(self):
        url = reverse('category-detail', args=[self.category.id])
        data = {'label': 'Updated Category'}
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.category.refresh_from_db()
        self.assertEqual(self.category.label, 'Updated Category')

    def test_delete_category(self):
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())
