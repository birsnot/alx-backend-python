from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Message.objects.none()

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You are not a participant of this conversation", code=status.HTTP_403_FORBIDDEN)

        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = Conversation.objects.get(conversation_id=conversation_id)

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You are not a participant of this conversation", code=status.HTTP_403_FORBIDDEN)

        serializer.save(sender=self.request.user, conversation=conversation)
