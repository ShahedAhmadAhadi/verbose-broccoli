from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Tweet
from .serializers import TweetSeializer
from rest_framework.parsers import JSONParser

# Create your views here.

def tweet(request):
    if request.method == 'GET':
        tweet = Tweet.objects.all()
        tweet_serializer = TweetSeializer(tweet, many=True)
        return Response(tweet_serializer.data)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        tweet_serializer = TweetSeializer(data=data)
        if tweet_serializer.is_valid():
            tweet_serializer.save()
            return Response(tweet_serializer.data)
        return Response(tweet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
