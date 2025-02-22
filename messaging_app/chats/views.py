from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Conversation, Message, User
from .pagination import MessagePagination
from .permissions import IsParticipantOfConversation
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer

# Get the user model
User = get_user_model()


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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return only the conversations where the authenticated user is a participant.
        """
        user = self.request.user
        return Conversation.objects.filter(participants=user)

    def get_object(self):
        """
        Return only the conversation that belongs to the current user.
        """
        user = self.request.user
        conversation_id = self.kwargs["pk"]
        obj = get_object_or_404(
            self.get_queryset(),
            conversation_id=conversation_id,
            conversation_owner=user,
        )
        return obj

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation.
            - Add the conversation owner to the participants.
            - Set the conversation owner to the current user. in the perform_create method
        """
        serializer = self.get_serializer(data=request.data)
        conversation_owner = self.request.user
        participants = serializer.initial_data.get("participants", [])

        # add the conversation owner to the participants
        if conversation_owner not in participants:
            serializer.initial_data["participants"].append(conversation_owner.user_id)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    # create a new conversation
    def perform_create(self, serializer):
        """
        Set the conversation owner to the current user.
        """
        conversation_owner = self.request.user
        serializer.save(conversation_owner=conversation_owner)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination

    def get_object(self):
        """
        Return only the message that belongs to the current user.
        """
        user = self.request.user
        message_id = self.kwargs["pk"]
        msg = get_object_or_404(self.get_queryset(), message_id=message_id, sender=user)
        return msg

    def get_queryset(self):
        """
        Return only the messages that belong to the current user conversation.
        """
        user = self.request.user
        conversation_pk = self.kwargs.get(
            "conversation_pk"
        )  # get conversation id from nested url
        conversation = get_object_or_404(Conversation, conversation_id=conversation_pk)
        return Message.objects.filter(sender=user, conversation=conversation)

    def perform_create(self, serializer):
        """
        Create a new message.
            - Set the sender_id to the current user.
            - Set the conversation_id to the conversation specified in the URL.
        """
        sender = self.request.user
        conversation_pk = self.kwargs.get(
            "conversation_pk"
        )  # get conversation id from nested url
        conversation = get_object_or_404(Conversation, conversation_id=conversation_pk)

        serializer.save(sender=sender, conversation=conversation)
