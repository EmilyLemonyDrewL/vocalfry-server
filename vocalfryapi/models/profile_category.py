from django.db import models
from .profile import Profile
from .category import Category

class ProfileCategory(models.Model):

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    