from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.views.generic import TemplateView
from django.shortcuts import render
from chat.models import Thread
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

class Registration(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration.html'

class HomeView(TemplateView):
    template_name = "home.html"
    def get(self, request):
        users = CustomUser.objects.all()
        threads = Thread.objects.all()
        args = {'users': users,
                'threads': threads}
        return render(request, self.template_name, args)

@csrf_exempt
def create_thread(request):
    json_data = json.loads(request.body)
    room  = json_data['room_id']
    users = json_data['users']
    user1_id = users[0]
    user2_id = users[1]
    if not Thread.objects.filter(users__id = user1_id).filter(
                                 users__id = user2_id).exists():
        thread = Thread(room_id = room)
        thread.save()
        thread.users.add(CustomUser.objects.get(id = user1_id),
                         CustomUser.objects.get(id = user2_id))
    else:
        room = Thread.objects.filter(users__id = user1_id).filter(
                                     users__id = user2_id).values_list(
                                     'room_id', flat=True)[0]

    data = {
        'room_id': room,
    }

    return JsonResponse(data)
