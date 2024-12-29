import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


# user Model that extends AbstractUser
class user(AbstractUser):
    class Roles(models.IntegerChoices):
        ADMIN = 1, "admin"
        HOST = 2, "host"
        GUEST = 3, "guest"

    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    phone_number = models.CharField(max_length=50, null=True)
    role = models.IntegerField(choices=Roles.choices)


# conversation Model
class conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    participants = models.ManyToManyField(user)
    created_at = models.DateTimeField(auto_now_add=True)


# message Model
class message(models.Model):
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    sender = models.ForeignKey(user, on_delete=models.CASCADE)
    conversation = models.ForeignKey(conversation, on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
