from django.test import TestCase
from rest_framework import status
from vocalfryapi.models import User, JobListing

class TestJobListings(TestCase):

    def setUp(self):
        self.user = User.objects.create(uid="12345", first_name="test", last_name="user", user_type=0)
        self.job_listing = JobListing.objects.create(
            lister=self.user,
            title="Test Job",
            description="Test description",
            location="Test Location name",
            listing_date="2024-08-24",
            company_website="https://companywebsite.com/application"
        )

    def test_retrieve_job_listing(self):
        url = f'/joblistings/{self.job_listing.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.job_listing.id)

    def test_list_job_listings(self):
        url = '/joblistings'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), JobListing.objects.count())

    def test_create_job_listing(self):
        data = {
            'listerId': self.user.uid,
            'title': "Test Job",
            'description': "Test description",
            'location': "Test Location name",
            'listing_date': "2024-08-24",
            'company_website': "https://companywebsite.com/application"
        }
        url = '/joblistings'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobListing.objects.count(), 2)

    def test_update_job_listing(self):
        data = {
            'listerId': self.user.uid,
            'title': "Updated Test Job",
            'description': "Updated Test description",
            'location': "Updated Test Location name",
            'listing_date': "2024-08-25",
            'company_website': "https://companywebsite.com/applications"
        }
        url = f'/joblistings/{self.job_listing.id}'
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.job_listing.refresh_from_db()
        self.assertEqual(self.job_listing.title, 'Updated Test Job')

    def test_delete_job_listing(self):
        url = f'/joblistings/{self.job_listing.id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(JobListing.objects.exists())
