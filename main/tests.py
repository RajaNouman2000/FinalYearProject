from django.test import TestCase
import websocket
import json

# Create your tests here.

def on_message(ws, message):
    data = json.loads(message)
    print("Received message:", data)
    
    
ws = websocket.WebSocketApp("ws://127.0.0.1:8000/ws/chat/")
ws.on_message = on_message

ws.run_forever()