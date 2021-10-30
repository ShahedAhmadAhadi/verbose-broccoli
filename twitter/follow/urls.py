from django.urls import path
from .views import follow

urlpatterns = [
    path('<str:username>/', follow)
]