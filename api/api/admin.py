from django.contrib import admin
from .models import Sensor, RawData

# Register your models here.

admin.site.register(RawData)
admin.site.register(Sensor)
