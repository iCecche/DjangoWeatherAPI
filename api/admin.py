from django.contrib import admin
from .models import Forecast, History

# Registration your models here.
admin.site.register(Forecast)

admin.site.register(History)