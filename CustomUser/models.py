from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, null = False, blank = False)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.username