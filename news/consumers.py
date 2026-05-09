import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_name = None
        self.count_users = 0


    async def connect(self):
        self.group_name = 'news_notifications'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        self.count_users += 1
        print(f'New connection: {self.channel_name}, total users: {self.count_users}')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        self.count_users -= 1
        print(f'Connection closed: {self.channel_name}, total users: {self.count_users}')

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({
            'message': data['message']
        }))

    async def send_notification(self, event):
        print("Sending notification to group:", self.group_name)
        print(event['message'])
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
