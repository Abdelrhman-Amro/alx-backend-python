from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from messaging_app.settings import AUTH_USER_MODEL

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer


class UserRegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # this will return the current user


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    #
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    # Get all messages for a conversation
    @action(methods=["GET"], detail=True)
    def conversation_messages(self, request, pk=None):
        conversation = Conversation.objects.get(pk=pk)
        messages = Message.objects.filter(conversation=conversation)
        serializer = MessageSerializer(messages, many=True)
        json = serializer.data
        return Response(json, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
