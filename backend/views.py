from django.http import JsonResponse
from .models import Measurement, Notification, Device
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

def get_measurements(request):
    data = list(
        Measurement.objects.values(
            "id", "device_id", "value", "timestamp"
        )
    )
    return JsonResponse(data, safe=False)


def get_notifications(request):
    data = list(
        Notification.objects.order_by("-created_at").values(
            "id", "device_id", "measurement_id", "message", "created_at", "is_acknowledged"
        )
    )
    return JsonResponse(data, safe=False)

@csrf_exempt
def receive_measurement(request):
    if request.method == "POST":
        data = json.loads(request.body)
        device = Device.objects.get(id = data["device"])
        Measurement.objects.create(
            device=device,
            value=data["power"],
            timestamp=datetime.now()
        )
        return JsonResponse({"status":"ok"})