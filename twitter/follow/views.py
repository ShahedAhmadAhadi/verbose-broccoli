from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.

def follow(request, username):
    data = request.data

    print(username)

    return Response({'result', username})
