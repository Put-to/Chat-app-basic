from django.shortcuts import render
from django.core.cache import cache

# Create your views here.


def lobby(request):
    return render(request, "chatapp/home.html")


def room(request, room_name):
    cache.get_or_set(room_name, 1)
    print(room_name)
    return render(
        request,
        "chatapp/room.html",
        {
            "room": {"name": room_name},
        },
    )
