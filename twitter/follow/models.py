from django.db import models

# Create your models here.

class Followers(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name="following")
    following_user_id = models.ForeignKey('User', related_name='followers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)