from django.conf.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("chats.urls")),
    path("auth/", include("chats.auth")),
]
