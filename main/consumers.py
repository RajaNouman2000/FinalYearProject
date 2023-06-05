from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "test_consumer_group"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

        # Send a connection message to the WebSocket client
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Hello connected'
        }))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        # Send a disconnection message to the WebSocket client
        self.send(text_data=json.dumps({
            'type': 'connection_disconnected',
            'message': 'You are now disconnected'
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")

        # Echo the received message back to the WebSocket client
        self.send(text_data=json.dumps({
            'type': 'data_received',
            'message': f'Received data: {message}'
        }))

    def send_message(self, message):
        # Send a message to the WebSocket client
        print('Send a message to the WebSocket client')
        self.send(text_data=json.dumps({
            'type': 'message_from_view',
            'message': message
        }))

    def data_received(self, event):
        # Event handler for data_received type
        print('Event handler for data_received type')
        message = event['message']
        print(message)
        self.send_message(message)

    def message_from_view(self, event):
        # Event handler for message_from_view type
        print('Event handler for data_received type')
        message = event['message']
        print(message)
        self.send_message(message)
