import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


# user_id (Primary Key, UUID, Indexed)
# first_name (VARCHAR, NOT NULL)
# last_name (VARCHAR, NOT NULL)
# email (VARCHAR, UNIQUE, NOT NULL)
# password_hash (VARCHAR, NOT NULL)
# User Model that extends AbstractUser
class user(AbstractUser):
    class Roles(models.IntegerChoices):
        ADMIN = 1, "admin"
        HOST = 2, "host"
        GUEST = 3, "guest"

    phone_number = models.CharField(max_length=50, null=True)
    role = models.IntegerField(choices=Roles.choices)

    # index user
    class Meta:
        indexes = [
            models.Index(fields=["username"], name="username_idx"),
        ]


# Conversation Model
class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    participants = models.ManyToManyField(user)
    created_at = models.DateTimeField(auto_now_add=True)


# Message Model
class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    sender = models.ForeignKey(user, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
