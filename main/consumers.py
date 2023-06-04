import json
import time
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):

    message = ['raja', 'nouman', 'bhatti', 'babar']

    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.room_group_name
        )
        self.accept()

        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Hello connected'
        }))

        self.send_message_periodically()

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def send_message_periodically(self):
        while True:
            # Read the JSON file
            with open('main/static/seismic_data.json', 'r') as file:
                data = json.load(file)

                # Loop through the key-value pairs in the JSON data
                for key, value in data.items():
                    # Send each key-value pair to the connected device
                    self.send_message(json.dumps({key: value}))
                    # Wait for 1 second between each key-value pair
                    time.sleep(60)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

        self.send(text_data=json.dumps({
            'type': 'connection_disconnected',
            'message': 'You are now disconnected'
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": 'data received'}))
