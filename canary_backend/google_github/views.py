import os
import json
import requests as req 
from urllib.parse import quote
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
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
    permission_classes = [permissions.AllowAny]  # For testing

    def get(self, request):
        print("GitHub Callback triggered")
        print("Request Query Params:", request.query_params)

        code = request.query_params.get('code')
        if not code:
            print("No code provided")
            return Response({"error": "Code not provided"}, status=status.HTTP_400_BAD_REQUEST)

        github_client_id = os.getenv('GITHUB_CLIENT_ID')
        github_client_secret = os.getenv('GITHUB_CLIENT_SECRET')
        token_url = 'https://github.com/login/oauth/access_token'

        # Prepare data to exchange code for an access token
        token_data = {
            'client_id': github_client_id,
            'client_secret': github_client_secret,
            'code': code,
        }
        print(f"TOKEN DATA: {token_data}")

        headers = {'Accept': 'application/json'}
        token_response = req.post(token_url, data=token_data, headers=headers)

        if token_response.status_code != 200:
            print(f"Failed to obtain access token: {token_response.content}")
            return Response({"error": "Failed to obtain access token"}, status=status.HTTP_400_BAD_REQUEST)

        # Extract the access token
        access_token = token_response.json().get('access_token')
        if not access_token:
            print("No access token received")
            return Response({"error": "No access token received"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch user info
        user_info_url = 'https://api.github.com/user'
        user_info_response = req.get(user_info_url, headers={'Authorization': f'token {access_token}'})
        
        if user_info_response.status_code != 200:
            print(f"Failed to fetch user info: {user_info_response.content}")
            return Response({"error": "Failed to fetch user info"}, status=status.HTTP_400_BAD_REQUEST)

        user_info = user_info_response.json()
        print(f"USER INFO: {user_info}")
        
        # Fetch email info
        email_info_url = 'https://api.github.com/user/emails'
        email_response = req.get(email_info_url, headers={'Authorization': f'token {access_token}'})

        if email_response.status_code == 200:
            email_data = email_response.json()
            primary_email = next((email['email'] for email in email_data if email.get('primary')), None)
        else:
            primary_email = None  # Handle this case if no email is found

        if not primary_email:
            print("Email not found or unavailable")
            return Response({"error": "Email not found"}, status=status.HTTP_400_BAD_REQUEST)

        print("Email Info URL:", email_info_url)
        print("Authorization Header:", f'token {access_token}')

        if email_info_response.status_code == 200:
            email_data = email_info_response.json()
            print(f"EMAIL DATA: {email_data}")

            email = next((e['email'] for e in email_data if e['primary']), None)
            if not email:
                print("No primary email found")
                return Response({"error": "No primary email found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print(f"Failed to retrieve email info: {email_info_response.content}")
            return Response({"error": "Failed to retrieve email information"}, status=status.HTTP_400_BAD_REQUEST)

        # Create or get the user
        username = user_info.get('login')
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email}
        )
        
        if created:
            print(f"User created: {username}")
        else:
            print(f"User already exists: {username}")

        user.auth_token = access_token  # Ensure to handle token storage securely
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
