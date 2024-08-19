from django.db import models
from .user import User

class Profile(models.Model):

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name_seen_on_profile = models.CharField(max_length=80)
    image_url = models.CharField(max_length=200)
    bio = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    above_18 = models.BooleanField(default=0)
    work_remote = models.BooleanField(default=0)
    demo_reel_url = models.CharField(max_length=200)
    email = models.EmailField(max_length=250)
    phone = models.CharField(max_length=12)
    