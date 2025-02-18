from rest_framework.permissions import BasePermission

from .models import Conversation


class IsParticipantOfConversation(BasePermission):

    def has_permission(self, request, view):
        """
        Check if the user is a participant of the conversation.
        """
        conversation_id = view.kwargs.get("conversation_pk")
        conversation = Conversation.objects.get(conversation_id=conversation_id)
        user = request.user
        participants = conversation.participants.all()

        return user in participants
