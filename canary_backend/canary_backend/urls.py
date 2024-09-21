from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/social/', include('dj_rest_auth.registration.urls')),
    path('auth/', include('google_github.urls'))
]
