from django.urls import path, include
from .views import GoogleLogin, LinkGitHub, GitHubCallbackView, GitHubRepositoriesView
from dj_rest_auth import urls as rest_auth_urls
from dj_rest_auth.registration import urls as rest_auth_registration_urls



urlpatterns = [
    path('', include(rest_auth_urls)),
    path('registration/', include(rest_auth_registration_urls)),
    path('google/', GoogleLogin.as_view(), name='google_login'), 
    path('github/', LinkGitHub.as_view(), name='link-github'),
    path('github/callback/', GitHubCallbackView.as_view(), name='github-callback'),
    path('api/github/repositories/', GitHubRepositoriesView.as_view(), name='github-repositories'),
    

]

#add: http://localhost:8000/auth/github/ (call back uri)