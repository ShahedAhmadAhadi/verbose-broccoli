from typing_extensions import Required
from rest_framework import serializers

class TweetSeializer(serializers.Serializer):
    id = serializers.IntergerField(read_only=True)
    user = serializers.charField(max_length = 32)
    text = serializers.charField(max_length = 160)
    created_at = serializers.DateTimeField()



