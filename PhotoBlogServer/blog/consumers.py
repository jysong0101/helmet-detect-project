from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "notifications"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        print("WebSocket connected")  # 연결 로그 추가

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print("WebSocket disconnected")  # 연결 해제 로그 추가

    async def send_notification(self, event):
        message = event["message"]
        print(f"Sending notification: {message}")  # 메시지 로그 추가
        await self.send(text_data=json.dumps({
            "message": message
        }))
