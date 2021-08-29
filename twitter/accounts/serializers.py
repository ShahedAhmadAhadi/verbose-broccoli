from enum import unique
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserElementryData
from rest_framework.parsers import JSONParser


def response_maker_validator(*args, **kwargs):
    response_dict = {}
    for i in kwargs:
        if i == "email":
            if kwargs[i] == None or kwargs[i] == "":
                response_dict[i] = "[This field is required]"
        elif i == "username":
            if kwargs[i] == None or kwargs[i] == "":
                response_dict[i] = "[This field is required]"
            elif not kwargs[i].isalnum():
                response_dict[
                    i
                ] = "[{response_dict[i]} can only be [0-9], [a-z], [A-Z]]"
        else:
            if kwargs[i] == None or kwargs[i] == "":
                response_dict[i] = "[This field is required]"
            elif not kwargs[i].isalpha():
                response_dict[i] = "[username can only be [a-z], [A-Z]]"

    return response_dict


def duplicate_email():
    pass

class UserElementryDataSerializer(serializers.Serializer):

    first_name = serializers.CharField(min_length=3, max_length=16)
    last_name = serializers.CharField(min_length=3, max_length=16)
    email = serializers.EmailField()

    # class Meta:
    #     model = User
    #     fields = ["first_name", "last_name", "email"]

    def validate_first_name(self, value):
        # first_name = value.get("first_name", "")

        if not value.isalpha():
            raise serializers.ValidationError('The username should only contain [a-z], [A-Z]')
        return value
    # def validate(self, attrs):
    #     last_name = attrs.get("last_name", "")
    #     email = attrs.get("email", "")

    #     if first_name.isalpha():
    #         raise serializers.ValidationError(
    #             'The username should only contain [a-z], [A-Z]'
    #         )

    #     return attrs    
        #  super().validate(attrs)
    # def validate(self, attrs):

    #     if UserElementryData.objects.filter(email=email):
    #         pass

    #     validation_response = response_maker_validator(
    #         first_name=first_name, last_name=last_name, email=email
    #     )

    #     # return validation_response or attrs
    #     print(validation_response)
    #     return validation_response

    def create(self, validated_data):
        return UserElementryData.objects.create(**validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
