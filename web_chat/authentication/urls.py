from django.urls import path, include
from . import views

urlpatterns = [
    path('registration/', views.Registration.as_view(), name='registration'),
    path('', include('django.contrib.auth.urls')),
]
