from rest_framework import serializers
from .models import UserInfo

class UserInfoSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    DOB = serializers.DateField()
    gender = serializers.CharField()
    about = serializers.CharField(max_length=255)
    image = serializers.ImageField()

    def create(self, validated_data):
        return UserInfo.objects.create(**validated_data)
