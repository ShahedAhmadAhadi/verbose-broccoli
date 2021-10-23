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

    def update(self, instance, validated_data):

        instance.user = validated_data.get('user', instance.user)
        instance.DOB = validated_data.get('DOB', instance.DOB)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.about = validated_data.get('about', instance.about)
        instance.image = validated_data.get('image', instance.image)
        # instance.save()

        return super().update(instance, validated_data)
