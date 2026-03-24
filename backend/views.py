from django.http import JsonResponse
from .models import Measurement, Notification


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