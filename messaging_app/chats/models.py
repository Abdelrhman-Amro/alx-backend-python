import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

### User Model ####
# user_id (Primary Key, UUID, Indexed)
# first_name (VARCHAR, NOT NULL)
# last_name (VARCHAR, NOT NULL)
# email (VARCHAR, UNIQUE, NOT NULL)
# password_hash (VARCHAR, NOT NULL)
# phone_number (VARCHAR, NULL)
# role (ENUM: 'guest', 'host', 'admin', NOT NULL)
# created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

# Create the user Model an extension of the Abstract user for values not defined in the built-in Django User model


class User(AbstractUser):
    USER_ROLES = [("guest", "Guest"), ("host", "Host"), ("admin", "Admin")]

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password_hash = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=20, null=True)
    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=["user_id"], name="user_id_idx"),
            models.Index(fields=["email"], name="email_idx"),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


### Conversation Model ###
# conversation_id (Primary Key, UUID, Indexed)
# participants_id (Foreign Key, references User(user_id)
# created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    participants_id = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="participants"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        indexes = [
            models.Index(fields=["conversation_id"], name="conversation_id_idx"),
        ]

    def __str__(self):
        return f"Conversation-ID: {self.conversation_id} created at {self.created_at}"


### Message Model ###
# message_id (Primary Key, UUID, Indexed)
# sender_id (Foreign Key, references User(user_id))
# message_body (TEXT, NOT NULL)
# sent_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender"
    )
    conversation = models.ForeignKey(
        "Conversation",
        on_delete=models.CASCADE,
        related_name="conversation_messages",
    )  # blank by default is
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        indexes = [
            models.Index(fields=["message_id"], name="message_id_idx"),
            models.Index(fields=["sender_id"], name="sender_id_idx"),
        ]

    def __str__(self):
        return f"Sender-ID: {self.sender_id} sent Message-ID: {self.message_id} at {self.sent_at}"
