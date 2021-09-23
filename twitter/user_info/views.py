from django.core import exceptions
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status
from .serializers import UserInfoSerializer

# Create your views here.

@api_view(['POST'])
def add_user_info(request):
    data = request.data
    serializer = UserInfoSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializers.save()

    return Response(status=status.HTTP_201_CREATED)
