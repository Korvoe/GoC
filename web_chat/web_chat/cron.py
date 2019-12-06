from django.core.management.base import BaseCommand, CommandError
from chat.models import Message
from authentication.models import CustomUser
from django.utils import timezone
import datetime

def delete_messages():
    messages = Message.objects.all()
    for message in messages:
        if message.expiration_time < timezone.now():
            message.delete()

def delete_users():
    users = CustomUser.objects.all()
    for user in users:
        if user.last_active < timezone.now() - datetime.timedelta(days=30):
            user.delete()
