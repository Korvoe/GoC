# chat/consumers.py
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Thread
import json
import datetime
from django.utils import timezone

User = get_user_model()

#This consumers works with the "room.html" and the reconnecting-websocket.
#It handles the received data, messages and saves them in the database. It
# sends the existing data from database to the 'room.html' template too.
class ChatConsumer(WebsocketConsumer):
    #Shows last 10 messages, that are written in the chat.
    def fetch_messages(self, data):
        messages = Message.last_10_messages(self.room_name)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    #Receives the user's input via websocket, connects it with thread,
    #that it belongs to  and saves it in the database. It then returns it back to
    #template, so it can show it.
    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(
            author=author_user,
            content=data['message'],
            thread=Thread.objects.get(room_id = data['room_id']),
            expiration_time=timezone.now() + datetime.timedelta(minutes=5))
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    #These two methods just convert messages to json format.
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result[::-1]

    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    #Establish the connection with websocket
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            })

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

    def send_message(self, message):
        self.send(text_data=json.dumps(message))
