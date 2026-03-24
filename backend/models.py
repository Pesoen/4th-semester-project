from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'users'


class Device(models.Model):
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.device_type})"


class Measurement(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="measurements")
    value = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.device.name} - {self.value} @ {self.timestamp}"


class Notification(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="notifications")
    measurement = models.ForeignKey(Measurement, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_acknowledged = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.device.name}: {self.message}"