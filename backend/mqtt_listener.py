import paho.mqtt.client as mqtt
import json
import datetime
import requests


def on_connect(client, userdata, flags, rc, properties):
    print("Connected to MQTT broker")
    client.subscribe("home/power")

def on_message(client, userdata, msg):
    timeStamp = datetime.datetime.now().strftime("%H:%M:%S")
    url = "http://localhost:8000/api/measurements/"
    data = json.loads(msg.payload.decode())
    data["time"] = timeStamp
    print("Device:", data["device"])
    print("power:", data["power"])
    print("Time:", timeStamp)
    try:
        requests.post(url,json=data)
        print(url)
    except requests.exceptions.ConnectionError:
        print("Fejl i at sende data til Django")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883)

client.loop_forever()