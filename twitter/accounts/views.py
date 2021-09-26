from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from rest_framework import serializers, status
from rest_framework import views
from rest_framework import response
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserElementryDataSerializer, EmailVerificationSerializer
from .models import UserElementryData, UserVerificationInfo
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.decorators import api_view
from django.urls import reverse
from .utils import send_email
from django.conf import settings
import jwt, socket
from datetime import datetime, timedelta ,timezone, tzinfo
from django.contrib.auth.models import User

# Create your views here.

def sending_verification_again(request):
    data = request.data

    user_data = UserElementryData.objects.get(email = data['email'])
    user_verification_info = UserVerificationInfo.objects.get(email = user_data)
    user_verification_info.email_requests = user_verification_info.email_requests + 1
    user_verification_info.save()
    try:
        time_delta = datetime.now(tzinfo=timezone.utc) - user_data.created_at 
        turn = user_verification_info.email_requests % 5 == 0 
        time_to_request_again = pow(user_verification_info.email_request / 5, 2) * 50
        if turn and time_delta < timedelta(minutes = time_to_request_again):
            return Response({'too_many': 'too_many_requests_please_try_again_later'})
        # user_data = UserElementryData.objects.filter(email = data['email'])
        sending_email(request, UserElementryData, user_verification_info.email)
        return Response({'email': 'sent_email'})
    except:
        return Response({'error': 'error_sending_email_please_try_later'})
        


@api_view(["POST"])
def register_phase_one(request):
    data = request.data

    if UserElementryData.objects.filter(email= data['email']):
        return sending_verification_again(request)
        # return Response({'email': 'send_again_verify_info'}, status=status.HTTP_409_CONFLICT)        

    if User.objects.filter(email = data['email']):
        return Response({'email': 'already_have_account_login'}, status=status.HTTP_409_CONFLICT)

    try:
        serializer = UserElementryDataSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        UserVerificationInfo.objects.create(email = UserElementryData.objects.get(email=user_data['email']))

        sending_email(request, UserElementryData, user_data['email'])

        return Response(user_data, status=status.HTTP_201_CREATED)
    except socket.gaierror:
        return Response({'error': 'server_error_email_can_not_be_send'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def sending_email(request, model, email):
    email = model.objects.get(email=email)
    token = RefreshToken.for_user(email).access_token


    current_site = get_current_site(request).domain
    relative_link = reverse('verify_email')

    absolute_url = 'http://'+current_site+relative_link+"?token="+str(token)
    email_body = 'Hi! '+email.first_name+' '+email.last_name+' Use the link below to verify your email \n'+absolute_url

    data = {'email_subject': 'Verify you E-mail', 'email_body': email_body, 'email_to':email.email}

    send_email(data)


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
            
            if User.objects.filter(username=data['username']):
                return Response({'username': 'choose_another_username'}, status=status.HTTP_409_CONFLICT)

            serializer = RegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            access = serializer.validated_data.get("access", None)
            refresh = serializer.validated_data.get("refresh", None)
            username = serializer.validated_data.get("username", None)

            if access is not None:
                response = Response({'access_token': access, "refresh": refresh, "username", username})

            email_data.delete()

            user_data = serializer.data

            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response({'email': 'Email_not_verified'}, status=status.HTTP_400_BAD_REQUEST)

    except jwt.ExpiredSignatureError:
        return Response({'error': 'Acctivition Expired'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.DecodeError:
        return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)



