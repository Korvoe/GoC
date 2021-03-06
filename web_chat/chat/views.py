from django.shortcuts import render
from django.http import Http404
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from chat.models import Thread
import json


@login_required
def room(request, room_name):
    if Thread.objects.filter(room_id=room_name).exists():
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name)),
            'username': mark_safe(json.dumps(request.user.username)),
            })
    else:
        raise Http404("Page not fould")
