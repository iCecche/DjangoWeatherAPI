from django.db import models
from CustomUser.models import CustomUser
# Create your models here.

class Forecast(models.Model):
    location = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"It's {self.description} in {self.location} ({self.temperature} C) on {self.date} at {self.time}"


class History(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    method = models.CharField(max_length=10, null=True, blank=True)
    endpoint = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at} - ({self.method} - {self.endpoint})"