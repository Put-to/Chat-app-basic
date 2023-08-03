from django.shortcuts import render
from django.core.cache import cache

# Create your views here.


def lobby(request):
    if not request.session.session_key:
        request.session.create()
    return render(
        request, "chatapp/home.html", {"session_id": request.session.session_key}
    )


def room(request):
    return render(
        request,
        "chatapp/room.html",
    )
