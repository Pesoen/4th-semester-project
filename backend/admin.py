from django.contrib import admin
from .models import Device, Measurement, User, Notification

admin.site.register(Device)
admin.site.register(Measurement)
admin.site.register(User)
admin.site.register(Notification)