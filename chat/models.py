from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Message(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender")
    recipient = models.ForeignKey(User,on_delete=models.CASCADE,related_name="recipient")
    sended_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text

class Thread(models.Model):
    myId = models.CharField(max_length=255,unique=True,db_index=True)
    user1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user1")
    user2 = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user2")
    messages = models.ManyToManyField(Message)

    def __str__(self) -> str:
        return self.myId


