from django.urls import path
from .views import get_measurements

urlpatterns = [
    path("measurements/", get_measurements),
]