from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserElementryDataSerializer
from .models import UserElementryData
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

# Create your views here.
@api_view(["POST"])
def register_phase_one(request):
    data = request.data
    serializer = UserElementryDataSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    user_data = serializer.data


    email = UserElementryData.objects.get(email=user_data['email'])
    token = RefreshToken.for_user(email).access_token


    current_site = get_current_site(request).domain
    relative_link = reverse('verify_email')
    data = {'domain': current_site.domain}

    absolute_url = 'http://'


    return Response(user_data, status=status.HTTP_201_CREATED)


def verify_email(request):
    pass