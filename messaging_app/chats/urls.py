from django.urls import include, path

# pip install drf-nested-routers
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register(r"conversations", views.ConversationViewSet)

messages_router = routers.NestedDefaultRouter(
    router, r"conversations", lookup="conversation"
)
messages_router.register(r"messages", views.MessageViewSet, basename="message")
# 'basename' is optional. Needed only if the same viewset is registered more than once


urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(messages_router.urls)),
]
