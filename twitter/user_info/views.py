import base64
from django.conf import settings
from django.core import exceptions
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import serializers, status
from .serializers import UserInfoSerializer
from .models import UserInfo
from rest_framework.parsers import JSONParser, BaseParser
import jwt
from django.contrib.auth.models import User

# Create your views here.

@api_view(["GET"])
def user_info(request, id):
    queryset = UserInfo.objects.filter(id = id)
    serializer = UserInfoSerializer(queryset, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def add_user_info(request, format=None):
    data = request.data
    access_token = request.headers.get("token")
    refresh_token = request.headers.get("refresh_token")

    if access_token:
        key = settings.SECRET_KEY
    else:
        return Response({'Error': "NO token found"}, status=status.HTTP_401_UNAUTHORIZED)


    payload = jwt.decode(access_token, key, algorithms=["HS512"])

    user = User.objects.filter(id= payload["user_id"])

    

    serializer = UserInfoSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    user_info = serializer.data

    return Response(user_info, status=status.HTTP_201_CREATED)

