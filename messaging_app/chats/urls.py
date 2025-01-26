from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"conversations", views.ConversationViewSet)
router.register(r"messages", views.MessageViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
