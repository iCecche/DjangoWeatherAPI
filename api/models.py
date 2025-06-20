from django.db import models
from django.utils import timezone
from CustomUser.models import CustomUser
from datetime import date
# Create your models here.

class Forecast(models.Model):
    location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"It's {self.description} in {self.location} ({self.temperature} C) on {self.date} at {self.time}"


class APICallRecord(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    last_call = models.DateField(default=timezone.now)

    def can_request_forecast(self):
        if self.user.is_premium:
            return True
        else:
            if self.last_call != date.today():
                self.count = 0
                self.last_call = date.today()
            return self.count < 10

    def increment_daily_requests(self):
        if not self.user.is_premium:
            today = date.today()
            if self.last_call != today:
                self.count = 0
                self.last_call = today
            self.count += 1
            self.save()