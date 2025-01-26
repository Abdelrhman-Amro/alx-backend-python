import uuid

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

    REQUIRED_FIELDS = ["email", "password_hash", "role"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=["user_id"], name="user_id_idx"),
            models.Index(fields=["email"], name="email_idx"),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
