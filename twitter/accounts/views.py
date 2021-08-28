from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserElementryDataSerializer
from .models import UserElementryData
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
@api_view(["POST"])
def register_phase_one(request):
    data = request.data
    serializer = UserElementryDataSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    user_data = serializer.data

    email = UserElementryData.objects.get(email=user_data['email'])

    token = RefreshToken.for_user(email)

    return Response(user_data, status=status.HTTP_201_CREATED)
