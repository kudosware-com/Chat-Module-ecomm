from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()



def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    ctx = User.objects.all()
    # for user in ctx["users"]:
    #     print(user.username)

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'users':ctx
    })