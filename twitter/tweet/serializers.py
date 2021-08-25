
from rest_framework import serializers

class TweetSeializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.CharField(max_length = 32)
    text = serializers.CharField(max_length = 160)
    created_at = serializers.DateTimeField()



