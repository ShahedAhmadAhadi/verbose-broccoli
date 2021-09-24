import base64
from django.core import exceptions
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import serializers, status
from .serializers import UserInfoSerializer
from .models import UserInfo
from rest_framework.parsers import JSONParser, BaseParser
from io import BytesIO

# Create your views here.

@api_view(["GET"])
def user_info(request, id):
    queryset = UserInfo.objects.filter(id = id)
    serializer = UserInfoSerializer(queryset, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def add_user_info(request, format=None):
    data = request.data

    serializer = UserInfoSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    user_info = serializer.data

    return Response(user_info, status=status.HTTP_201_CREATED)

