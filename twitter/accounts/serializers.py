from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserElementryData

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=8, write_only=True)

    class Meta:
        model = UserElementryData
        fields = ['first_name', 'last_name', 'email']