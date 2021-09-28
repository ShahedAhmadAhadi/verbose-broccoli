from rest_framework import serializers
from .models import UserInfo
from django.contrib.auth.models import User

class UserInfoSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    DOB = serializers.DateField()
    gender = serializers.CharField()
    about = serializers.CharField(max_length=255)
    image = serializers.ImageField()

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)

    def create(self, validated_data):
        print(validated_data)
        return UserInfo.objects.create(**validated_data)
