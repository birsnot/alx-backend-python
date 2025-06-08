from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Conversation, Message

class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to participants of a conversation.
    """

    def has_permission(self, request, view):
        # Authenticated users only
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # If the object is a Message, check if user is part of its conversation
        if isinstance(obj, Message):
            return user in obj.conversation.participants.all()

        # If the object is a Conversation, check directly
        if isinstance(obj, Conversation):
            return user in obj.participants.all()

        return False
