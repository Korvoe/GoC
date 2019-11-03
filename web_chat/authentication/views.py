from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.views.generic import TemplateView
from django.shortcuts import render
# Create your views here.

class Registration(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration.html'

class HomeView(TemplateView):
    template_name = "home.html"
    def get(self, request):
        users = CustomUser.objects.all()

        args = {'users': users}
        return render(request, self.template_name, args)
