from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from rest_framework import serializers, status
from rest_framework import views
from rest_framework import response
from rest_framework.response import Response
from .serializers import (
    RegisterSerializer,
    UserElementryDataSerializer,
    EmailVerificationSerializer,
)
from .models import UserElementryData, UserVerificationInfo
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.decorators import api_view
from django.urls import reverse
from .utils import send_email
from django.conf import settings
import jwt, socket
from datetime import datetime, timedelta, timezone, tzinfo
from django.contrib.auth.models import User
from twitter import func
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict


# Create your views here.


def sending_verification_again(request):
    data = request.data

    user_data = UserElementryData.objects.get(email=data["email"])
    user_verification_info = UserVerificationInfo.objects.get(email=user_data)
    print(user_data)
    try:
        time_delta = datetime.now(tz=timezone.utc) - user_data.created_at
        turn = user_verification_info.email_requests > 5
        time_to_request_again = pow(user_verification_info.email_requests / 5, 2) * 50
        print(turn)
        print(time_delta, timedelta(minutes=time_to_request_again))
        if turn and time_delta < timedelta(minutes=time_to_request_again):
            return Response({"too_many": "too_many_requests_please_try_again_later"})

        user_verification_info.email_requests = (
            user_verification_info.email_requests + 1
        )
        user_verification_info.save()
        user_data = UserElementryData.objects.filter(email=data["email"])
        sending_email(request, UserElementryData, user_verification_info.email)
        return Response({"email": "sent_email"})
    except:
        return Response({"error": "error_sending_email_please_try_later"})


@api_view(["POST"])
def register_phase_one(request):
    data = request.data

    if UserElementryData.objects.filter(email=data["email"]):
        return sending_verification_again(request)
        # return Response({'email': 'send_again_verify_info'}, status=status.HTTP_409_CONFLICT)

    if User.objects.filter(email=data["email"]):
        return Response(
            {"email": "already_have_account_login"}, status=status.HTTP_409_CONFLICT
        )

    try:
        serializer = UserElementryDataSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        UserVerificationInfo.objects.create(
            email=UserElementryData.objects.get(email=user_data["email"])
        )

        sending_email(request, UserElementryData, user_data["email"])

        return Response(user_data, status=status.HTTP_201_CREATED)
    except socket.gaierror:
        return Response(
            {"error": "server_error_email_can_not_be_send"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def sending_email(request, model, email):
    email = model.objects.get(email=email)
    token = RefreshToken.for_user(email).access_token

    current_site = get_current_site(request).domain
    relative_link = reverse("verify_email")

    absolute_url = "http://" + current_site + relative_link + "?token=" + str(token)
    email_body = (
        "Hi! "
        + email.first_name
        + " "
        + email.last_name
        + " Use the link below to verify your email \n"
        + absolute_url
    )

    data = {
        "email_subject": "Verify you E-mail",
        "email_body": email_body,
        "email_to": email.email,
    }

    send_email(data)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):

        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS512")
            print(payload, "payload")
            user = UserElementryData.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response(
                {"email": "Successfully_activated?" + str(user)},
                status=status.HTTP_200_OK,
            )
            # return HttpResponseRedirect(redirect_to='http://localhost:3000?token='+token)

        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Acctivition Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {"error": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(["POST"])
def register_phase_two(request):
    try:
        token = request.GET.get("token")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS512")
        email_data = UserElementryData.objects.get(id=payload["user_id"])
        if email_data.is_verified:
            data = request.data
            data["email"] = email_data.email
            data["first_name"] = email_data.first_name
            data["last_name"] = email_data.last_name

            if User.objects.filter(username=data["username"]):
                return Response(
                    {"username": "choose_another_username"},
                    status=status.HTTP_409_CONFLICT,
                )

            serializer = RegisterSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            user_data = serializer.data

            def get_token(user):
                token = RefreshToken.for_user(user)
                return token

            def token_(user):
                print(user)
                refresh = get_token(user)
                data["refresh"] = str(refresh)
                data["access"] = str(refresh.access_token)
                data["username"] = user

                return data

            data_token = token_(User.objects.filter(username=user_data["username"])[0])
            print(data_token)
            access = data_token["access"]
            refresh = data_token["refresh"]
            username = data_token["username"].username

            email_data.delete()

            if access is not None:
                response = Response(
                    {
                        "access_token": access,
                        "refresh": refresh,
                        "username": username,
                        "user_data": user_data,
                    },
                    status=status.HTTP_201_CREATED,
                )
                response.set_cookie("token", access, httponly=True)
                response.set_cookie("refresh", refresh, httponly=True)
                response.set_cookie("username", username, httponly=True)
                return response

            return Response(
                {"error": "something_went_wrong__try_again!"},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"email": "Email_not_verified"}, status=status.HTTP_400_BAD_REQUEST
        )

    except jwt.ExpiredSignatureError:
        return Response(
            {"error": "Acctivition Expired"}, status=status.HTTP_400_BAD_REQUEST
        )
    except jwt.exceptions.DecodeError:
        return Response({"error": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST", "GET"])
def prac(request):

    if request.method == "GET":
        http_cookie = request.META.get("HTTP_COOKIE")

        auth_info_dict = func.cookie_value_to_dict(http_cookie)
        # print(request.META)

        auths = func.auth_user_tokens(auth_info_dict)
        response = Response({'auths': 'auths'})
        try:
            response.set_cookie('token', auths['token'], httponly=True)
            return response
        except:
            return response.content({auths})
        

    if request.method == "POST":
        data = request.data
        user = authenticate(username=data['username'], password=data['password'])

        refresh_tokens = RefreshToken.for_user(user)

        refresh = str(refresh_tokens)
        access = str(refresh_tokens.access_token)
        username = user.username

        data.pop('password')

        if access and refresh:
            response = Response({'username': user.username}, status=status.HTTP_200_OK)
            response.set_cookie("token", access, httponly=True)
            response.set_cookie("refresh", refresh, httponly=True)
            response.set_cookie("username", username, httponly=True)
            return response

        return Response(user)

            

    # refresh_token = request.headers.get("refresh")
    # key = settings.SECRET_KEY
    # print((access_token.get('token')))
    # return Response(key)
    # try:
        
    #     payload = jwt.decode(access_token, key, algorithms=["HS512"])

    #     user = User.objects.filter(id= payload["user_id"])
    #     print(user)
    #     # ["access_token"]
    #     # ["HTTP_COOKIE"]
    #     # for i in data: 
    #     #     print(i)
    #     return Response({'result': 'done'})
    # except jwt.ExpiredSignatureError:
    #     payload = jwt.decode(refresh_token, key, algorithms=['HS512'])
    #     user = User.objects.filter(id = payload["user_id"])
    #     return Response(user[0].username)

