from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

@api_view(['POST'])
def add_user_info(request):
    print('yes')
    return Response(status=status.HTTP_201_CREATED)
