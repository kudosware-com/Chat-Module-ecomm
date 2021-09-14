from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = User.objects.all()

    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,
    })

def room(request, room_name):
    ctx = User.objects.all()
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'users':ctx
    })