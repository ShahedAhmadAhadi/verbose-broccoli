from rest_framework import serializers

class UserInfoSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    DOB = serializers.DateField()
    gender = serializers.CharField()
    about = serializers.CharField(max_length=255)
    image = serializers.ImageField()
