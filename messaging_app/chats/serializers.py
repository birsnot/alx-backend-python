from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'user_id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_preview = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'message_preview',
            'sent_at',
        ]

    def get_message_preview(self, obj):
        return obj.message_body[:30] + "..." if len(obj.message_body) > 30 else obj.message_body


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages',
            'created_at',
        ]

    def validate(self, data):
        if not data.get('participants'):
            raise serializers.ValidationError("A conversation must have at least one participant.")
        return data
