from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from rest_framework import serializers, status
from rest_framework import views
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserElementryDataSerializer, EmailVerificationSerializer
from .models import UserElementryData
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.decorators import api_view
from django.urls import reverse
from .utils import send_email
from django.conf import settings
import jwt

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

    absolute_url = 'http://'+current_site+relative_link+"?token="+str(token)
    email_body = 'Hi! '+email.first_name+' '+email.last_name+' Use the link below to verify your email \n'+absolute_url

    data = {'email_subject': 'Verify you E-mail', 'email_body': email_body, 'email_to':email.email}

    send_email(data)


    return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS512')
            print(payload, 'payload')
            user=UserElementryData.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
 
            return Response({'email': 'Successfully_activated?'+str(user)}, status=status.HTTP_200_OK)
            # return HttpResponseRedirect(redirect_to='http://localhost:3000?token='+token)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Acctivition Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_phase_two(request):
    try:
        token = request.GET.get('token')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS512')
        email_data=UserElementryData.objects.get(id=payload['user_id'])
        if email_data.is_verified:
            data = request.data
            data['email'] = email_data.email
            data['first_name'] = email_data.first_name
            data['last_name'] = email_data.last_name
            serializer = RegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            user_data = serializer.data
            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response({'email': 'Email_not_verified'}, status=status.HTTP_400_BAD_REQUEST)
        


        
        
    except:
        return 
    data = request.data
    serializer = RegisterSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    print(data)
    user_data = serializer.data
    return Response(user_data, status=status.HTTP_201_CREATED)



        