import json
from channels.generic.websocket import AsyncWebsocketConsumer


waiting_users = set()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["session"].session_key
        if len(waiting_users) > 0:
            self.room_group_name = waiting_users.pop()
            first = False
        else:
            self.room_group_name = f"chat_{self.user_id}"
            waiting_users.add(self.room_group_name)
            first = True
        print(waiting_users)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        print(first)

        if first:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "connect",
                        "user_id": self.user_id,
                        "message": "You are Alone here",
                    }
                )
            )
        else:
            self.send_initial_messages()

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "disconnect",
                "user_id": "nil",
                "message": "Your chat partner has disconnected.",
            },
        )
        waiting_users.discard(self.room_group_name)
        await self.close(code=4020)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        user_id = self.user_id
        await self.send_initial_messages()

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "user_id": user_id, "message": message},
        )

    async def chat_message(self, event):
        message = event["message"]
        user_id = event["user_id"]
        await self.send(
            text_data=json.dumps(
                {"type": "chat_message", "user_id": user_id, "message": message}
            )
        )

    async def send_initial_messages(self):
        self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "connect",
                "user_id": self.user_id,
                "message": "Stranger has Connected",
            },
        )
