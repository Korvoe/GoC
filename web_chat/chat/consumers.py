# chat/consumers.py
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Thread
import json
import rsa
from django.conf import settings

User = get_user_model()
# TEMPORARY, we should probably declare that elsewhere !
(pub_key, priv_key) = (settings.PUB_KEY, settings.PRIV_KEY)
print("public key (n, e) :(" + str(pub_key.n) + ") ; (" + str(pub_key.e) +")\n")
print("private key (n, e, d, p, q) :(" + str(priv_key.n) + ") ; (" + str(priv_key.e) + ") ; (" + str(priv_key.d) + ") ; (" + str(priv_key.p) + ") ; (" + str(priv_key.q) + ") \n")
# need to share the public key with the clients !

class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        messages = Message.last_10_messages(self.room_name)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(
            author=author_user,
            content=data['message'],
            thread=Thread.objects.get(room_id = data['room_id']))
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

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
        # Decryption of the ciphertext : message is a string
        if text_data != '{\"command\":\"fetch_messages\"}' :
            print(text_data + str(type(text_data)))
            encodedCipher = text_data.encode('utf8')
            print(str(encodedCipher) + str(type(encodedCipher)))
            message = rsa.decrypt(encodedCipher, priv_key)
            print(message.decode('utf8'))
        else:
            message = text_data

        data = json.loads(message)
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
