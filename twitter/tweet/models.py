from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE

# Create your models here.


class Tweet(models.Model):
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    text = models.CharField(max_length=160)
    created_at = models.DateTimeField(auto_now_add=True)
