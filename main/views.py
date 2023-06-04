from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def home(request):
    return render(request, "main/index.html")


@csrf_exempt
def sensor(request):
    if request.method == 'POST':
        # Assuming the sensor sends data in the request body as JSON
        data = request.POST.get('sensor_data')

        return HttpResponse('data not received')
    elif request.method == 'GET':
        return HttpResponse('From GET method')
    else:
        return HttpResponse('Method not allowed.', status=405)
