from rest_framework import serializers

from .models import Conversation, Message, User


class UserSerializer(serializers.ModelSerializer):
    ### custom validators
    def validate_phone_number(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits")
        return value

    full_name = serializers.SerializerMethodField()
    phone_number = serializers.CharField(
        max_length=10, validators=[validate_phone_number], required=False
    )

    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "full_name",
            "phone_number",
            "role",
            "created_at",
        ]
        read_only_fields = ("user_id", "created_at")
        write_only_fields = ("password",)

    def create(self, validated_data):
        password = validated_data.pop("password", None)  # get password
        instance = self.Meta.model(**validated_data)  # create user instance
        if password:
            instance.set_password(password)  # this will hash the password and update
        instance.save()  # save user instance
        return instance

    # overriding update method
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)  # get password
        print(instance)
        # update password
        if password:
            instance.set_password(password)  # this will hash the password and update
        return super().update(instance, validated_data)

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation
        fields = ["conversation_id", "conversation_owner", "created_at", "participants"]
        read_only_fields = ("conversation_id", "created_at", "conversation_owner")

    def validate_participants(self, value):
        """
        ✅Ensure that there are at least 2 participants in the conversation.
        🧠Remember that the conversation owner is automatically added as a participant.
        """
        if len(value) < 2:
            raise serializers.ValidationError("You must add at least 1 participant.")
        return value


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
