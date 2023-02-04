from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/gs', views.get_status, name='get_status'),
]