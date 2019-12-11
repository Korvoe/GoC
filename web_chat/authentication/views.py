from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.views.generic import TemplateView
from django.shortcuts import render
from chat.models import Thread
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

#Sends form to registration template and in case of proper
#registration redirects user to login.
class Registration(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration.html'

#Handle get response by sending the set of all users and threads(rooms) back to template.
class HomeView(TemplateView):
    template_name = "home.html"
    def get(self, request):
        users = CustomUser.objects.all()
        threads = Thread.objects.all()
        args = {'users': users,
                'threads': threads}
        return render(request, self.template_name, args)

@csrf_exempt
#The creation of room. Function receives randomly
#generated room number and user ids of users in the room.
#It then creates the thread, if it didn't exist yet. If it exists,
#it just changes the "room" variable to the existing thread value and, after all,
#returns the room id.
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

@csrf_exempt
#When user logs in, this function is called in order to
#set his last_active status to current time.
def last_active(request):
    json_data = json.loads(request.body)
    user_id = json_data['user']
    if CustomUser.objects.filter(id = user_id).exists():
        User = CustomUser.objects.get(id = user_id)
        User.last_active = timezone.now()
        User.save()

    data = {'1': 1,}
    return  JsonResponse(data)
