import os
import json
from urllib.parse import quote
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from .serializers import UserSerializer
from .models import User, GitHubRepository
from google.oauth2 import id_token
from google.auth.transport import requests


load_dotenv()

class LinkGitHub(SocialLoginView):
    def get(self, request):
        print("TRIGGER LINK GITHUB VIEW")
        github_client_id = os.getenv('GITHUB_CLIENT_ID')
        print(f" CLIENT ID: {github_client_id} ")
        redirect_uri = quote("http://127.0.0.1:8000/auth/github/callback/" )
        url = (
            f"https://github.com/login/oauth/authorize"
            f"?client_id={github_client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&scope=repo"
        )
        return JsonResponse({'url': url})

class GitHubCallbackView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({"error": "Code not provided"}, status=status.HTTP_400_BAD_REQUEST)

        github_client_id = os.getenv('GITHUB_CLIENT_ID')
        github_client_secret = os.getenv('GITHUB_CLIENT_SECRET')
        token_url = 'https://github.com/login/oauth/access_token'
        token_data = {
            'client_id': github_client_id,
            'client_secret': github_client_secret,
            'code': code,
        }
        headers = {'Accept': 'application/json'}
        token_response = requests.post(token_url, json=token_data, headers=headers)
        
        if token_response.status_code != 200:
            return Response({"error": "Failed to obtain access token"}, status=status.HTTP_400_BAD_REQUEST)

        access_token = token_response.json().get('access_token')
        if not access_token:
            return Response({"error": "No access token received"}, status=status.HTTP_400_BAD_REQUEST)

        # Store access token in the user's profile
        user = request.user
        user.auth_token = access_token  
        user.save()

        return Response({"message": "GitHub account linked successfully"}, status=status.HTTP_200_OK)

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


# class GitHubWebhookView(APIView):
#     permission_classes = [AllowAny]

#     @csrf_exempt
#     def post(self, request):
#         payload = json.loads(request.body)
#         event_type = request.headers.get('X-GitHub-Event')
#         repo_name = payload.get('repository', {}).get('name')
#         repo_url = payload.get('repository', {}).get('html_url')

#         # Find or create the repository
#         repo, _ = GitHubRepository.objects.get_or_create(
#             repo_name=repo_name,
#             repo_url=repo_url,
#             user=request.user  # Assuming user can be inferred
#         )

#         # Parse events
#         if event_type == 'push':
#             for commit in payload.get('commits', []):
#                 GitHubEvent.objects.create(
#                     repository=repo,
#                     event_type='push',
#                     message=commit.get('message'),
#                     author=commit.get('author', {}).get('name'),
#                 )

#         elif event_type == 'pull_request':
#             action = payload.get('action')
#             pull_request = payload.get('pull_request', {})
#             GitHubEvent.objects.create(
#                 repository=repo,
#                 event_type='pull_request' if action != 'closed' else 'pull_request_merged',
#                 message=pull_request.get('title'),
#                 url=pull_request.get('html_url'),
#                 author=pull_request.get('user', {}).get('login'),
#             )

#         return JsonResponse({'message': 'Webhook processed successfully'}, status=status.HTTP_200_OK)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    permission_classes = [permissions.AllowAny]

    def post(self, request):
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
