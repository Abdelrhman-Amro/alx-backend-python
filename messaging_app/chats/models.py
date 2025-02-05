import uuid

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models


# User
class User(AbstractUser):
    """
    A user of the chat service.
    """

    USER_ROLES = [("guest", "Guest"), ("host", "Host"), ("admin", "Admin")]

    # Fields
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password_hash = models.CharField(max_length=128, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default="guest",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    date_joined = None  # Removing defdate_joined field

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=["user_id"], name="user_id_idx"),
            models.Index(fields=["email"], name="email_idx"),
        ]
        swappable = "AUTH_USER_MODEL"

    def __str__(self):
        return f"{self.username}"


# Conversation
class Conversation(models.Model):
    """
    A conversation between two or more users.
    """

    # Fields
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Relationships
    conversation_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_conversations",
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="conversations",
    )

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        indexes = [
            models.Index(fields=["conversation_id"], name="conversation_id_idx"),
        ]

    def __str__(self):
        return f"{self.conversation_owner} {self.conversation_id} CONVERSATION"


# Message
class Message(models.Model):
    """
    A message sent by a user in a conversation.
    """

    # Fields
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    # Relationships
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conversation = models.ForeignKey(
        "Conversation",
        on_delete=models.CASCADE,
        related_name="messages",
    )

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        indexes = [
            models.Index(fields=["message_id"], name="message_id_idx"),
            models.Index(fields=["sender"], name="sender_idx"),
        ]

    def __str__(self):
        return f"{self.sender} SENT_TO {self.conversation} "
