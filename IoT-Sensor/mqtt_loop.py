#!/usr/bin/env python3



import paho.mqtt.client as mqtt
import json
import socket
import time
import datetime
import random


# Define Variables
MQTT_HOST = "192.168.58.3"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "sensor/md"
count = 0

while count < 2:
    posix_now = time.time()
    utc_tsd = datetime.datetime.utcnow()
    value1 = (random.randint(0, 999))
    value2 = (random.randint(0, 999))

    MQTT_MSG = json.dumps({"host": socket.gethostname(),
                           "unix_time": int(time.time()),
                           "utc_time": datetime.datetime.now().isoformat(),
                           "value_1": (random.randint(0, 999)),
                           "value_2": (random.randint(0, 99)),
                           "value_3": (random.randint(50, 100))}
                          );
    print(MQTT_MSG)
    print(count)


    def on_publish(client, userdata, mid):
        print("done" - MQTT_HOST)


    def on_connect(client, userdata, flags, rc):
        client.subscribe(MQTT_TOPIC)
        client.publish(MQTT_TOPIC, MQTT_MSG, qos=1, retain=True)


    def on_message(client, userdata, msg):
           client.disconnect()


    # Initiate MQTT Client
    mqttc = mqtt.Client()

    # Register publish callback function
    mqttc.on_publish = on_publish
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    # Connect with MQTT Broker
    mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

    # Loop forever
    mqttc.loop_forever()

    count += 1

print("end")
