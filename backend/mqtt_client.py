import json
import os
import django
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "4TH-SEMESTER-PROJECT.settings")
django.setup()

from backend.models import Device, Measurement

import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPIC = "devices/+/power"


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())

        device_id = data["device_id"]
        value = data["power"]

        device = Device.objects.get(id=device_id)

        Measurement.objects.create(
            device=device,
            value=value,
            timestamp=datetime.now()
        )

        print(f"Saved measurement for device {device_id}")

    except Exception as e:
        print("Error:", e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


def start():
    client.connect(BROKER, 1883, 60)
    client.loop_forever()