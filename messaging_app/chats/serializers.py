from rest_framework import serializers

from .models import Conversation, Message, User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "user_name",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "password_hash",
            "phone_number",
            "role",
            "created_at",
        ]

        def get_full_name(self, obj):
            return f"{obj.first_name} {obj.last_name}"


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
