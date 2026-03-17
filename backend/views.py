from django.http import JsonResponse
from .models import Measurement


def get_measurements(request):
    data = list(
        Measurement.objects.values(
            "id", "device_id", "value", "timestamp"
        )
    )
    return JsonResponse(data, safe=False)