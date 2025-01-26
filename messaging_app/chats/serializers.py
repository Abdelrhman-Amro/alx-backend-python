from rest_framework import serializers

from .models import Conversation, Message, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "created_at",
        ]


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants_id", "created_at"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["message_id", "sender_id", "conversation_id", "sent_at", "content"]
