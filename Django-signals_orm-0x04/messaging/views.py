from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    user = request.user
    logout(request)        # Log the user out first
    user.delete()          # Triggers post_delete signal
    return redirect('/')   # Redirect to homepage (or your goodbye page)
