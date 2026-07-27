from django.db import models

class SensorData(models.Model):
    apikey = models.CharField(max_length=50)
    device_id = models.CharField(max_length=50)
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device_id} at {self.timestamp}"
