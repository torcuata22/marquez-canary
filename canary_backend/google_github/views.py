import os
import json
import requests as req 
from urllib.parse import quote
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount, SocialToken
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.providers.github.provider import GitHubProvider
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from dj_rest_auth.registration.views import SocialLoginView
from .serializers import UserSerializer
from .models import User, GitHubRepository
from google.oauth2 import id_token
from google.auth.transport import requests


load_dotenv()
github_client_id = os.getenv('GITHUB_CLIENT_ID')
github_client_secret = os.getenv('GITHUB_CLIENT_SECRET')

class LinkGitHub(SocialLoginView):
    def get(self, request):
        github_client_id = os.getenv('GITHUB_CLIENT_ID')
        github_client_secret = os.getenv('GITHUB_CLIENT_SECRET')
        print("TRIGGER LINK GITHUB VIEW")

        redirect_uri = quote("http://127.0.0.1:8000/auth/github/callback/" )
        scope = "user:email"

        url = (
            f"https://github.com/login/oauth/authorize"
            f"?client_id={github_client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&scope={scope}"
        )
        return JsonResponse({'url': url})



class GitHubCallbackView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        code = request.query_params.get('code')
        print(f"CODE: {code}")
        if not code:
            return Response({"error": "Code not provided"}, status=status.HTTP_400_BAD_REQUEST)

        github_client_id = os.getenv('GITHUB_CLIENT_ID')
        github_client_secret = os.getenv('GITHUB_CLIENT_SECRET')
        token_url = 'https://github.com/login/oauth/access_token'

        # Exchange code for access token
        token_data = {
            'client_id': github_client_id,
            'client_secret': github_client_secret,
            'code': code,
        }

        headers = {'Accept': 'application/json'}
        token_response = req.post(token_url, data=token_data, headers=headers)

        if token_response.status_code != 200:
            return Response({"error": "Failed to obtain access token"}, status=status.HTTP_400_BAD_REQUEST)

        access_token = token_response.json().get('access_token')
        if not access_token:
            return Response({"error": "No access token received"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch user info
        user_info_url = 'https://api.github.com/user'
        user_info_response = req.get(user_info_url, headers={'Authorization': f'token {access_token}'})

        if user_info_response.status_code != 200:
            return Response({"error": "Failed to fetch user info"}, status=status.HTTP_400_BAD_REQUEST)

        user_info = user_info_response.json()
        
        # Get GitHub username
        github_username = user_info.get('login', '').lower()
        if not github_username:
            return Response({"error": "GitHub username not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch email info
        email_info_url = 'https://api.github.com/user/emails'
        email_response = req.get(email_info_url, headers={'Authorization': f'token {access_token}'})

        primary_email = None
        if email_response.status_code == 200:
            email_data = email_response.json()
            primary_email = next((email['email'] for email in email_data if email.get('primary')), None)

        # Find or create the user
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=github_username,
            defaults={'email': primary_email or 'default@example.com'}
        )
        print(f"USER: {user.username}, Created: {created}")

        account,created_account = SocialAccount.objects.get_or_create(
            user=user,
            provider='github',
            defaults={'uid': user_info.get('id'), 'extra_data': user_info}
        )

        # Link the social account
        try:
            account = SocialAccount.objects.get(user=user, provider='github')
            SocialToken.objects.create(
                account=account,
                token=access_token,
                
            )
        except SocialAccount.DoesNotExist:
            return Response({"error": "Social account does not exist"}, status=status.HTTP_404_NOT_FOUND)
        if access_token:
            frontend_url = f'http://127.0.0.1:8080/githubrepos?token={access_token}'
            return redirect(frontend_url)
        else:
            return JsonResponse({'error': 'Token not received'}, status=400)

        
        # return Response({"message": "GitHub account linked successfully", "token": access_token}, status=status.HTTP_200_OK)
        
# class GitHubCallbackView(APIView):
#     def get(self, request):
#         code = request.GET.get('code')
#         client_id = os.getenv('GITHUB_CLIENT_ID')
#         client_secret = os.getenv('GITHUB_CLIENT_SECRET')

#         # Exchange code for an access token
#         token_response = requests.post(
#             'https://github.com/login/oauth/access_token',
#             data={
#                 'client_id': client_id,
#                 'client_secret': client_secret,
#                 'code': code
#             },
#             headers={'Accept': 'application/json'}
#         )
#         token_json = token_response.json()
#         access_token = token_json.get('access_token')

        # if access_token:
        #     # Redirect the user to the frontend, passing the token
        #     frontend_url = f'http://127.0.0.1:8080/githubrepos?token={access_token}'
        #     return redirect(frontend_url)
        # else:
        #     return JsonResponse({'error': 'Token not received'}, status=400)


class GitHubRepositoriesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        auth_token = user.auth_token  # Ensure your user model has this field
        print("Authenticated User:", user)
        print("User Model:", type(user)) 

        if not auth_token:
            return Response({"error": "GitHub account not linked"}, status=status.HTTP_400_BAD_REQUEST)

        headers = {
            'Authorization': f'token {auth_token}',
            'Accept': 'application/vnd.github.v3+json',
        }
        response = requests.get('https://api.github.com/user/repos', headers=headers)

        if response.status_code == 200:
            return Response(response.json(), status=200)
        else:
            return Response({'error': 'Failed to fetch repositories'}, status=response.status_code)


class SelectRepositoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        repo_name = request.data.get('repo_name')
        repo_url = request.data.get('repo_url')

        if not repo_name or not repo_url:
            return Response({"error": "Repository name and URL are required"}, status=status.HTTP_400_BAD_REQUEST)

        GitHubRepository.objects.create(
            user=request.user,
            repo_name=repo_name,
            repo_url=repo_url
        )

        return Response({"message": "Repository selected and saved"}, status=status.HTTP_201_CREATED)


class GitHubWebhookView(APIView):
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        payload = json.loads(request.body)
        event_type = request.headers.get('X-GitHub-Event')
        repo_name = payload.get('repository', {}).get('name')
        repo_url = payload.get('repository', {}).get('html_url')

        # Find or create the repository
        repo, _ = GitHubRepository.objects.get_or_create(
            repo_name=repo_name,
            repo_url=repo_url,
            user=request.user  # Assuming user can be inferred
        )

        # Parse events
        if event_type == 'push':
            for commit in payload.get('commits', []):
                GitHubEvent.objects.create(
                    repository=repo,
                    event_type='push',
                    message=commit.get('message'),
                    author=commit.get('author', {}).get('name'),
                )

        elif event_type == 'pull_request':
            action = payload.get('action')
            pull_request = payload.get('pull_request', {})
            GitHubEvent.objects.create(
                repository=repo,
                event_type='pull_request' if action != 'closed' else 'pull_request_merged',
                message=pull_request.get('title'),
                url=pull_request.get('html_url'),
                author=pull_request.get('user', {}).get('login'),
            )

        return JsonResponse({'message': 'Webhook processed successfully'}, status=status.HTTP_200_OK)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        print("TRIGGER GOOGLE LOGIN VIEW")
        token_string = request.data.get('id_token')
        print(f"TOKEN: {token_string}")

        if not token_string:
            return Response({"error": "ID token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            client_id = os.getenv('GOOGLE_CLIENT_ID')
            id_info = id_token.verify_oauth2_token(token_string, requests.Request(), client_id)
            print("ID Info:", id_info)

            email = id_info['email']
            name = id_info.get('name', '')
            user_id = id_info.get('sub')

            # Fetch or create user based on email
            user, created = User.objects.get_or_create(
                username=email,
                defaults={'username': email, 'first_name': name}
            )
            print(f"USER: {user}, Created: {created}")
            print(f"Fetched user: {user}, ID: {user.id}, Email: {user.email}")

            # Fetch or create social account
            social_account, social_created = SocialAccount.objects.get_or_create(
                user_id=user.id,
                provider='google',
                uid=user_id,
                defaults={'extra_data': id_info}
            )

            if social_created:
                print(f"Created new social account for {user.email}")
            else:
                print(f"Social account exists for {user.email}")
            
        
            # Prepare the response data
            data = {
                'user_id': user.id,
                'email': user.email,
                'username': user.username,
                'name': id_info.get('name', ''),
            }

            return Response({"user_data": data}, status=status.HTTP_200_OK)

        except ValueError as e:
            print("Error verifying token:", e)
            return Response({"error": "Invalid ID token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Unexpected error:", e)
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
