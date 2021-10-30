from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(['GET'])
def follow(request, username):
    data = request.data

    print(username)

    return Response({'result': username})
