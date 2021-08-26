from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework import response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import Tweet
from .serializers import TweetSeializer
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class DemoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print(request.headers)
        return Response({'success': 'you are authenticated'})

@api_view(['GET', 'POST'])
def tweet(request):
    if request.method == 'GET':
        tweet = Tweet.objects.all()
        serializer = TweetSeializer(tweet, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        tweet_serializer = TweetSeializer(data=data)
        if tweet_serializer.is_valid():
            tweet_serializer.save()
            return Response(tweet_serializer.data)
        return Response(tweet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
