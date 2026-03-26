from django.urls import path
from .views import get_measurements, get_notifications, receive_measurement

urlpatterns = [
    path("measurements/", get_measurements),
    path("notifications/", get_notifications),
    path("api/measurements/receive/", receive_measurement),
]