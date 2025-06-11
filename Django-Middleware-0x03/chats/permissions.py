from rest_framework import permissions
from .models import Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    - Allows only authenticated users
    - Allows only participants to interact with conversation messages
    - Allows only the sender to edit/delete messages
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Message):
            # All participants can view or send messages
            if request.method in permissions.SAFE_METHODS or request.method == "POST":
                return request.user in obj.conversation.participants.all()
            # Only sender can update/delete
            elif request.method in ["PUT", "PATCH", "DELETE"]:
                return obj.sender == request.user
        return False
