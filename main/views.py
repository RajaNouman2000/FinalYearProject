from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


@csrf_exempt
def home(request):
    return render(request, "main/index.html")


@csrf_exempt
def sensor(request):
    global onemint  # Declare the variable as global

    if request.method == 'POST':
        if 'onemint' not in globals():
            onemint = []  # Initialize the variable if it doesn't exist

        data = json.loads(request.body)
        onemint.append(data)

        if len(onemint) == 6000:
            # Send data to ChatConsumer
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "test_consumer_group",
                {
                    "type": "send_message",
                    "message": onemint
                }
            )
            print(onemint)
            onemint = []

        return HttpResponse('Data received and sent to ChatConsumer')
    else:
        return HttpResponse('Method not allowed.', status=405)
