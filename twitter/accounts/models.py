from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserElementryData(models.Model):
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    email = models.EmailField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class UserVerificationInfo(models.Model):
    email = models.OneToOneField(UserElementryData, on_delete=models.CASCADE)
    email_requests = models.IntegerField(default=1)



