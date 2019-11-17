from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Thread(models.Model):
    room_id = models.IntegerField()
    users = models.ManyToManyField(User)

class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username

    def last_10_messages(room_number):
        return Message.objects.filter(thread__room_id=room_number).order_by('-timestamp').all()[:10]
