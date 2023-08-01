from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from chatapp.consumers import ChatConsumer

websocket_urlpatterns = [path("ws/chat/<str:room_name>/", ChatConsumer.as_asgi())]
