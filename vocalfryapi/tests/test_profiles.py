from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from vocalfryapi.models import Profile, User, ProfileCategory, Category

class TestProfiles(TestCase):

    def setUp(self):
        
        self.category = Category.objects.create(id=1, label="Test Category")

        # create User for profile test
        self.user = User.objects.create(uid="12345", first_name="test", last_name="user", user_type=0)

        self.profile = Profile.objects.create(
            user=self.user,
            name_seen_on_profile="Test name",
            image_url="imagetest.jpg",
            bio="Test bio",
            location="Nashville",
            above_18=True,
            work_remote=True,
            demo_reel_url="demoreellink.mp3",
            email="testemail@gmail.com",
            phone="615-111-1111"
        )

        # create profilecategory for profile test
        self.category = ProfileCategory.objects.create(category=self.category, profile=self.profile)

        self.url = reverse('profile-list')
        self.profile_detail_url = reverse('profile-detail', args=[self.profile.id])

    def test_retrieve_profile(self):
        response = self.client.get(self.profile_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name_seen_on_profile'], self.profile.name_seen_on_profile)
        self.assertEqual(response.data['user']['uid'], self.user.uid)

    def test_list_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name_seen_on_profile'], self.profile.name_seen_on_profile)

    def test_list_profiles_by_category(self):
        response = self.client.get(self.url, {'category_id': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name_seen_on_profile'], self.profile.name_seen_on_profile)

    def test_create_profile(self):
        
        new_user_for_test = User.objects.create(
            uid="54321",
            first_name="Test",
            last_name="User",
            user_type=0
        )
        url = reverse('profile-list')
        data = {
          'userId': new_user_for_test.uid,
          'name_seen_on_profile': 'Test',
          'image_url': 'image.jpg',
          'bio': "blah blah blah bio test",
          'location': "Nashville, TN",
          "above_18": True,
          "work_remote": True,
          "demo_reel_url": "http://testdemoreel.com/demo.mp3",
          "email": "testemail@gmail.com",
          "phone": "615-111-1111"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name_seen_on_profile'], data['name_seen_on_profile'])

    def test_update_profile(self):
        url = reverse('profile-detail', args=[self.profile.id])
        data = {
          'userId': self.user.uid,
          'name_seen_on_profile': 'Voice Lady',
          'image_url': 'image3.jpg',
          'bio': "bio test lorem ipsum",
          'location': "California",
          "above_18": True,
          "work_remote": False,
          "demo_reel_url": "http://testdemoreel.com/reel.mp3",
          "email": "testemail3@gmail.com",
          "phone": "615-111-2222"
        }
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        updated_profile = Profile.objects.get(pk=self.profile.id)
        self.assertEqual(updated_profile.name_seen_on_profile, data['name_seen_on_profile'])

    def test_delete_profile(self):
        url = reverse('profile-detail', args=[self.profile.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Profile.objects.filter(pk=self.profile.id).exists())
