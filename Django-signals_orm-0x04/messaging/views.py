from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from .models import Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User


@login_required
def delete_user(request):
    user = request.user
    logout(request)        # Log the user out first
    user.delete()          # Triggers post_delete signal
    return redirect('/')   # Redirect to homepage (or your goodbye page)


@login_required
def conversation_with_user(request, username):
    target_user = User.objects.get(username=username)

    messages = Message.objects.filter(
        sender=request.user, receiver=target_user
    ).union(
        Message.objects.filter(sender=target_user, receiver=request.user)
    ).select_related('sender', 'receiver', 'parent_message'
                     ).prefetch_related('replies'
                                        ).order_by('timestamp')

    return render(request, 'messaging/conversation.html', {
        'messages': messages,
        'target_user': target_user
    })


@require_POST
@login_required
def send_message(request):
    receiver_username = request.POST['receiver']
    content = request.POST['content']
    parent_id = request.POST.get('parent_message')

    receiver = get_object_or_404(User, username=receiver_username)

    parent = None
    if parent_id:
        parent = get_object_or_404(Message, id=parent_id)

    Message.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content,
        parent_message=parent
    )

    return HttpResponseRedirect(f'/messages/{receiver_username}/')


@login_required
def unread_inbox(request):
    unread_messages = Message.unread.unread_for_user(
        request.user).only('id', 'sender', 'content', 'timestamp')

    return render(request, 'messaging/unread_inbox.html', {
        'unread_messages': unread_messages
    })
