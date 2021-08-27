from django.db import models

# Create your models here.

class UserElementryData(models.Model):
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    email = models.EmailField(max_length=255, unique=True)
    
