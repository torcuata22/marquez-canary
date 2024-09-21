from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    auth_token = models.CharField(max_length=255, blank=True, null=True)  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.email

  