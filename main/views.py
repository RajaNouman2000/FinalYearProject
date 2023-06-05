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
    if request.method == 'POST':
        # Assuming the sensor sends data in the request body as JSON
        data = json.loads(request.body)
        print(data)

        # Send data to ChatConsumer
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "test_consumer_group",
            {
                "type": "send_message",
                "message": data
            }
        )

        return HttpResponse('Data received and sent to ChatConsumer')
    else:
        return HttpResponse('Method not allowed.', status=405)
