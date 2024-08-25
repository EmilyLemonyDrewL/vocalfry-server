from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from vocalfryapi.models import Category, Profile, ProfileCategory, User

class TestProfileCats(TestCase):

    def setUp(self):
        self.user = User.objects.create(uid="12345", first_name="test", last_name="user", user_type=0)
        self.profile = Profile.objects.create(user=self.user, name_seen_on_profile="Test Name")
        self.category = Category.objects.create(label="Test Category")
        self.profile_category = ProfileCategory.objects.create(profile=self.profile, category=self.category)

    def test_retrieve_profile_cat(self):
        url = f'/profilecategories/{self.profile_category.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.profile_category.id)

    def test_list_profile_cats(self):
        url = '/profilecategories'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), ProfileCategory.objects.count())

    def test_create_profile_cat(self):
        data = {
            'profile': self.profile.id,
            'category': self.category.id
        }
        url = '/profilecategories'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProfileCategory.objects.count(), 2)

    def test_delete_profile_cat(self):
        url = f'/profilecategories/{self.profile_category.id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ProfileCategory.objects.exists())
