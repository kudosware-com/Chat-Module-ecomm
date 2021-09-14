import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Thread,Message
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

User = get_user_model()

class ChatConsumer(AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def getUser(self,user1,user2):
        self.user2 =  User.objects.get(username=user2)
        self.room_group_name = ""
        if(user1.username > self.user2.username):
            self.room_group_name += self.user2.username + "_"
            self.room_group_name += (user1.username + '_chat')
        else:
            self.room_group_name += user1.username + "_"
            self.room_group_name += (self.user2.username + '_chat')

        return self.user2

    @database_sync_to_async
    def getInitialMessages(self):
        messages = Thread.objects.get(myId=self.room_group_name).messages.all()
        parsed_messages = []
        for message in messages:
            tp = {}
            tp["text"] = message.text
            tp["sender"] = message.sender.username
            tp["recipient"] = message.recipient.username
            parsed_messages.append(tp)
        return parsed_messages


    async def connect(self):
        self.user1 = self.scope['user']
        self.user2 = self.scope['url_route']['kwargs']['user_name']
        self.user2 = await self.getUser(self.user1, self.user2)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_add(self.room_group_name ,self.channel_name)
        await self.accept()


        messages = await self.getInitialMessages()
        await self.send_json(
            {
                'type': 'initial_messages',
                'message': messages
            }  
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive_json(self, text_data):
        message = text_data
        print(self.user1.username,self.user2.username)
        msg = await self.saveMessage(message["message"],self.user1,self.user2)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': msg.text,
                'user':msg.sender.username
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

        return msg
        
    async def chat_message(self, event):
        message = event['message']
        
        await self.send_json({
            'type':"chat_message",
            'sender': event['user'],
            'message': message
        })