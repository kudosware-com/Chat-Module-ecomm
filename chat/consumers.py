import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Thread,Message
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

User = get_user_model()

class ChatConsumer(AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def getUser(self,user2):
        return User.objects.get(username=user2)

    async def connect(self):
        self.user1 = self.scope['user']
        self.user2 = self.scope['url_route']['kwargs']['user_name']
        self.user2 = await self.getUser(self.user2)
        self.room_group_name = "as"
        # if(self.user1.username > self.user2.username):
        #     self.room_group_name += self.user2.username
        #     self.room_group_name += (self.user1.username + '_chat')

        # else:
        #     self.room_group_name += self.user1.username
        #     self.room_group_name += (self.user2.username + '_chat')

        # self.myThread = Thread.objects.get(myId=self.room_group_name)
        # self.messages = self.myThread.messages
        # for message in self.messages:
        #     print(message)
        
        # Join room group
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )
        await self.channel_layer.group_add(self.room_group_name ,self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive_json(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        message = text_data

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        

    # Receive message from room group
    @database_sync_to_async
    def saveMessage(self,message,sender,recipient):
        msg = Message(text=message,sender=sender,recipient=recipient)
        msg.save()
        self.threadName = ""
        if(self.user1.username < self.user2.username):  
            self.threadName = self.user1.username 
            self.threadName += '_'
            self.threadName += self.user2.username
            self.threadName += '_chat'
            thread,_ = Thread.objects.get_or_create(user1=self.user1,user2=self.user2,myId=self.threadName)
            print(type(thread.messages))        
            thread.messages.add(msg)
            thread.save()
        else:
            self.threadName = self.user2.username
            self.threadName += '_'
            self.threadName += self.user1.username
            self.threadName += '_chat'
            thread,_ = Thread.objects.get_or_create(user2=self.user1,user1=self.user2,myId=self.threadName)        
            thread.messages.add(msg)
            thread.save()
        


    async def chat_message(self, event):
        message = event['message']["message"]
        
        # Send message to WebSocket
        await self.saveMessage(message,self.user1,self.user2)
        await self.send(text_data=json.dumps({
            'message': message
        }))