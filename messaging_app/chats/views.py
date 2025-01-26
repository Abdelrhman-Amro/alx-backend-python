from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filters = [filters.SearchFilter, filters.OrderingFilter]


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filters = [filters.SearchFilter, filters.OrderingFilter]

    # Get all messages for a conversation
    @action(methods=["GET"], detail=True)
    def conversation_messages(self, request, pk=None):
        conversation = Conversation.objects.get(pk=pk)
        messages = Message.objects.filter(conversation=conversation)
        serializer = MessageSerializer(messages, many=True)
        json = serializer.data
        return Response(json, status=status.HTTP_200_OK)
