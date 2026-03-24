from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #forside
    path('', views.main, name='main'),
    #devices
    path('devices/', views.device_list, name='device_list'),
    path('devices/create/', views.device_create, name='device_create'),
    path('devices/<int:pk>/edit/', views.device_edit, name='device_edit'),
    path('devices/<int:pk>/delete/', views.device_delete, name='device_delete'),
    #measurement
    path('measurements/', views.measurement_list, name='measurement_list'),
    path('measurements/create/', views.measurement_create, name='measurement_create'),
    path('measurements/<int:pk>/edit/', views.measurement_edit, name='measurement_edit'),
    path('measurements/<int:pk>/delete/', views.measurement_delete, name='measurement_delete'),
    #Login/Logout stuff.
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]