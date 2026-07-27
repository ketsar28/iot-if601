from django.contrib import admin
from .models import SensorData

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'temperature', 'humidity', 'timestamp')
    list_filter = ('device_id',)
    search_fields = ('device_id', 'apikey')
