from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserElementryData


def response_maker_validator(*args, **kwargs):
    


class UserElementryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def validate(self, attrs):
        first_name = attrs.get('first_name', '')
        last_name = attrs.get('last_name', '')
        email = attrs.get('email', '')

        if not first_name.isalpha():
            raise serializers.ValidationError('The first_name should only be in [a-z, A-Z]')
        if not last_name.isalpha():
            raise serializers.ValidationError('The last_name should only be in [a-z, A-Z]')

        return attrs

    def create(self, validated_data):
        return UserElementryData.objects.create(**validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']