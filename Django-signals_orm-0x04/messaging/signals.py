from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Only if the message already exists (not being created)
        try:
            original = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return

        if original.content != instance.content:
            # Save old content to history
            MessageHistory.objects.create(
                message=original,
                old_content=original.content,
                edited_by=original.sender,
            )
            instance.edited = True  # Mark message as edited


@receiver(post_delete, sender=User)
def clean_up_user_related_data(sender, instance, **kwargs):
    # Delete messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications for the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories tied to those messages
    # (In case CASCADE didn't handle them already)
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
