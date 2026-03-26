from django.db import models
from django.contrib.auth.models import User as AuthUser


class Device(models.Model):
    device_id = models.CharField(max_length=100)#was "name"
    type = models.CharField(max_length=50)
    custom_name = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        display = self.custom_name if self.custom_name else self.id
        return f"{display} ({self.type})"


class Measurement(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="measurements")
    value = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.device.id} - {self.value} @ {self.timestamp}"


class Notification(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="notifications")
    measurement = models.ForeignKey(Measurement, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_acknowledged = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.device.id}: {self.message}"