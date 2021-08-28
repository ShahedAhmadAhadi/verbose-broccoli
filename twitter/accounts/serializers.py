from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserElementryData
from rest_framework.parsers import JSONParser


def response_maker_validator(*args, **kwargs):
    response_dict = {}
    for i in kwargs:
        if i == 'username' or i == 'email':
            if kwargs[i] == None or kwargs[i] == '':
                response_dict[i] = '[This field is required]'
        elif i == 'username':
            if not kwargs[i].isalnum():
                response_dict[i] = '[{response_dict[i]} can only be [0-9], [a-z], [A-Z]]'
        else:
            if kwargs[i] == None or kwargs[i] == '':
                response_dict[i] = '[This field is required]'
            elif not kwargs[i].isalpha():
                response_dict[i] = '[username can only be [a-z], [A-Z]]'

    return response_dict
        


class UserElementryDataSerializer(serializers.ModelSerializer):

    

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    # def validate(self, attrs):
    #     first_name = attrs.get('first_name', '')
    #     last_name = attrs.get('last_name', '')
    #     email = attrs.get('email', '')

    #     if not first_name.isalpha():
    #         raise serializers.ValidationError('The first_name should only be in [a-z, A-Z]')
    #     if not last_name.isalpha():
    #         raise serializers.ValidationError('The last_name should only be in [a-z, A-Z]')

    #     return attrs

    def validate(self, attrs):
        first_name = attrs.get('first_name', '')
        last_name = attrs.get('last_name', '')
        email = attrs.get('email', '')
        print(first_name)
        validation_response =  response_maker_validator(first_name=first_name, last_name=last_name, email=email)
        
        return validation_response

    def create(self, validated_data):
        return UserElementryData.objects.create(**validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']