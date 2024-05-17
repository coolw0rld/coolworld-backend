from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.create, name = 'create'),
    path('verify/', views.verify, name = 'verify'),
    path('stamp/', views.stamp, name='stamp'),
]