from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserElementryData


def response_maker_validator(*args, **kwargs):
    response_dict = {}
    for i in kwargs:
        response_dict_key = response_dict[i]
        if i == 'username':
            if not kwargs[i].isalnum():
                response_dict_key = '[{response_dict_key} can only be [0-9], [a-z], [A-Z]]'
        elif i == 'username' or i == 'email':
            if kwargs[i] == None or kwargs[i] == '':
                response_dict_key = '[This field is required]'
        else:
            if kwargs[i] == None or kwargs[i] == '':
                response_dict_key = '[This field is required]'
            elif not kwargs[i].isalpha():
                response_dict_key = '[username can only be [a-z], [A-Z]]'
        


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