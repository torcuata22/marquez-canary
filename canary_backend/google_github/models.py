from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


#custom User with auth_token for GitHub auth
class User(AbstractBaseUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    auth_token = models.CharField(max_length=255, blank=True, null=True)  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.email

#Model to store infromation on selected GitHub Repositories
class GitHubRepository(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    repo_name = models.CharField(max_length=255)
    repo_url = models.URLField()
    event = models.CharField(max_length=255, blank=True, null=True)  
    retrieved_at = models.DateTimeField(auto_now_add=True)   

  