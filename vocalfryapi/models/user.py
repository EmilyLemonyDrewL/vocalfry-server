from django.db import models

class User(models.Model):

    uid = models.CharField(max_length=50)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_type = models.BooleanField(default=0)
    