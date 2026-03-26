import paho.mqtt.client as mqtt
import json
import datetime
import requests


def on_connect(client, userdata, flags, rc, properties):
    #Print statement to tell if connected
    print("Connected to MQTT broker")
    #The MQTT "link" we subscribe to
    client.subscribe("home/power")

def on_message(client, userdata, msg):
    #Time for when message is sent, NOT when the measurement is taken
    timeStamp = datetime.datetime.now().strftime("%H:%M:%S")
    #Endpoint for the data, that will be used in Django
    url = "http://localhost:8000/api/measurements/receive/"
    #The data we get via MQTT
    data = json.loads(msg.payload.decode())
    #Add the time value
    data["time"] = timeStamp
    #Print in here to see right data
    print("Device:", data["device"])
    print("power:", data["power"])
    print("Time:", timeStamp)
    #Try and send it to Django
    try:
        requests.post(url,json=data)
    except requests.exceptions.ConnectionError:
        print("Fejl i at sende data til Django")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883)

client.loop_forever()