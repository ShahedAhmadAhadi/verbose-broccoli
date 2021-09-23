from django.contrib import admin
from django.urls import path, include
from .views import add_user_info

urlpatterns = [
    path('add/', add_user_info)
]