from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
import json
from django.conf import settings
import rsa

# Create your views here.

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'public_key_n': settings.PUB_KEY.n,
    })
