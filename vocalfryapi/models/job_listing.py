from django.db import models
from .user import User

class JobListing(models.Model):

    lister = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=50)
    listing_date = models.DateField()
    company_website = models.CharField(max_length=200)
    