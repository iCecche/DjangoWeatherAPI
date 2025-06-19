from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, null = False, blank = False)
    is_premium = models.BooleanField(default=False)
    daily_requests = models.IntegerField(default=0)
    last_request_date = models.DateField(default=date.today())

    def can_request_forecast(self):
        if self.is_premium:
            return True
        else:
            if self.last_request_date != date.today():
                self.daily_requests = 0
                self.last_request_date = date.today()
            return self.daily_requests < 10

    def increment_daily_requests(self):
        if not self.is_premium:
            today = date.today()
            if self.last_request_date != today:
                self.daily_requests = 0
                self.last_request_date = today
            self.daily_requests += 1
            self.save()