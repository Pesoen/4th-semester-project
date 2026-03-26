from django.urls import path
from .views import get_measurements, get_notifications

urlpatterns = [
    path("measurements/", get_measurements),
    path("notifications/", get_notifications),
]