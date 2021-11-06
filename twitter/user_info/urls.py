from django.contrib import admin
from django.urls import path, include
from .views import add_user_info, user_info, user_info_data


urlpatterns = [
    path("add/", add_user_info),
    path("user-info/<int:id>/", user_info),
    path("user-info/<str:property>", user_info_data),
]
