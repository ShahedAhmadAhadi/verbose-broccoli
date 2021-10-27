import base64
from django.conf import settings
from django.core import exceptions
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import serializers, status
from .serializers import UserInfoSerializer
from .models import UserInfo
from rest_framework.parsers import JSONParser, BaseParser
import jwt
from django.contrib.auth.models import User
from twitter import func

# Create your views here.


@api_view(["GET"])
def user_info(request, id):
    queryset = UserInfo.objects.filter(id=id)
    serializer = UserInfoSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["POST", "PATCH"])
def add_user_info(request, format=None):
    data = request.data
    
    if request.method == "PATCH":
        auths = func.auth_user_request(request)
        username = auths["data"]["username"]
        print(auths["response"], auths["condition"])
        user = User.objects.get(username = username)
        user_info = UserInfo.objects.get(user = user.id)
        print(user_info, 'userinfp')
        # data.update({'user': user_info.id})
        serializer = UserInfoSerializer(instance = user_info, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            auths["data"].update(serializer.data)
            auths["response"].data = auths["data"]
            return auths["response"]
        return auths["response"]

    # http_cookie = request.META.get("HTTP_COOKIE")

    # dict_user_authentications = func.cookie_value_to_dict(http_cookie)

    # auths = func.auth_user_tokens(dict_user_authentications)

    auths = func.auth_user_request(request)
    print(auths["response"], auths["condition"])
    if auths["condition"]:
        # http_cookie = request.META.get("HTTP_COOKIE")
        # auths["response"].data.update(func.cookie_value_to_dict(http_cookie))
        user = User.objects.get(username = auths["data"]["username"])
        print(user.id)
        data.update({'user': user.id})
        serializer = UserInfoSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_info = serializer.data
        auths["response"].data = user_info
        print(user_info)
        return auths["response"]
    else:
        return auths["response"]

    # print(auths)
    return Response("a")
    # if auths == dict_user_authentications

    if access_token:
        key = settings.SECRET_KEY
    else:
        return Response(
            {"Error": "NO token found"}, status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        payload = jwt.decode(access_token, key, algorithms=["HS512"])
        print(payload)

        user = User.objects.filter(id=payload["user_id"])

        data["user"] = user[0].id
        print(user[0].id)


        return Response(user_info, status=status.HTTP_201_CREATED)

    except jwt.ExpiredSignatureError:
        pass


@api_view(["GET"])
def user_info_data(request, property):
    # data = request.data

    auths = func.auth_user_request(request)
    username = auths["data"]["username"]
    print(auths["response"], auths["condition"])
    user = User.objects.get(username = username)

    # user_data = {}
    # user_data.update(UserInfo.objects.get(user = user.id))
    user_data = UserInfo.objects.filter(user = user.id)
    serializer = UserInfoSerializer(user_data, many=True)
    print(serializer.data[0][property])
    try:
        pass
    except:
        pass

    return Response({'e': user.username})


