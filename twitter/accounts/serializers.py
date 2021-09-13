from enum import unique
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserElementryData
from rest_framework.parsers import JSONParser


def duplicate_email():
    pass

class UserElementryDataSerializer(serializers.Serializer):

    first_name = serializers.CharField(min_length=3, max_length=16)
    last_name = serializers.CharField(min_length=3, max_length=16)
    email = serializers.EmailField()

    def validate_first_name(self, value):

        if not value.isalpha():
            raise serializers.ValidationError('The username should only contain [a-z], [A-Z]')
        return value
    def validate_last_name(self, value):

        if not value.isalpha():
            raise serializers.ValidationError('The username should only contain [a-z], [A-Z]')
        return value

    def create(self, validated_data):
        return UserElementryData.objects.create(**validated_data)


class RegisterSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=64, min_length=8, write_only=True)
    username = serializers.CharField(max_length=64, min_length=5)
    first_name = serializers.CharField(min_length=3, max_length=16)
    last_name = serializers.CharField(min_length=3, max_length=16)
    email = serializers.EmailField()

    def validate_username(self, value):
        for i in value:
            if not 65 <= ord(i) <= 90 or 97 <= ord(i) <= 122 or ord(i) == 95 or ord(i) == 36:
                raise serializers.ValidationError('The username should only contain [a-z], [A-Z], [1-9], $, _')          


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=1000)


