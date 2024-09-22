from django.contrib import admin
from .models import User, GitHubRepository

admin.site.register(User)
admin.site.register(GitHubRepository)

