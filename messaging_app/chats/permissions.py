from rest_framework import permissions

class IsConversationParticipant(permissions.BasePermission):
    """
    Only allow participants of the conversation to access it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()

class IsMessageParticipant(permissions.BasePermission):
    """
    Only allow participants of the conversation related to the message.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.conversation.participants.all()
