from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

# Auth URLs
urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh_token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
]
