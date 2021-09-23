from django.db import models
from django.contrib.auth.models import User

# Create your models here.

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female')
]

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DOB = models.DateField(null=False)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6)
    about = models.TextField(max_length=255)
    image = models.ImageField(upload_to='userImages')

    def __str__(self) -> str:
        return self.user.username
