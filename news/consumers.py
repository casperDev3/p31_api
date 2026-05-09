import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    #     self.group_name = None

    async def connect(self):
        self.group_name = 'news_notifications'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({
            'message': data['message']
        }))

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
