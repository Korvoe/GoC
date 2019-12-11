from django.db import models
from django.contrib.auth import get_user_model
from authentication.models import EncryptedCharField

User = get_user_model()

#The thread model, which is the chat "room", that makes the relations between messages and users.
class Thread(models.Model):
    room_id = models.IntegerField()
    users = models.ManyToManyField(User)

#The message, which is related to User and Thread models. It has got expiration_time,
#which is the lifetime of the message. If the message is expired, it is deleted by the cron.
class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = EncryptedCharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    expiration_time = models.DateTimeField()

    def __str__(self):
        return self.author.username

    def last_10_messages(room_number):
        return Message.objects.filter(thread__room_id=room_number).order_by('-timestamp').all()[:10]
