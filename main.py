#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time

from wiserble import WiserDimmer

dimmerAddress = "90:FD:9F:5C:XX:XX"
mqttBroker = "192.168.1.XXX"
mqttPort = 1883

# Set Room Name for Dimmer to be used in topics
room = "bedroom"

# Connect to the Dimmer
dimmer = WiserDimmer(dimmerAddress)

client = mqtt.Client("WiserDimmer")
client.connect(mqttBroker, int(mqttPort))
client.loop_start()

def SetBrightness(client, userdata, message):
    # Set brightness
    print("Brightness set to: " + str(message.payload.decode()))
    print(int(message.payload.decode()))
    dimmer.level_set(int(message.payload.decode()))

def SetState(client, userdata, message):
    print("Switch set to: " + str(message.payload.decode("utf-8")))
    # Switch State
    if (str(message.payload.decode("utf-8")) == "ON"):
        dimmer.state_on()
    else:
        dimmer.state_off()

# Callback functions to run when receiving topics
client.message_callback_add(room + "/light/brightness/set", SetBrightness)
client.message_callback_add(room + "/light/switch", SetState)

# Subscribe to topics
client.subscribe(room + "/light/#")

# Loop through and publish state and brightness
while True:
    client.publish(room + "/light/status", dimmer.state)
    client.publish(room + "/light/brightness", dimmer.level)
    time.sleep(1)

client.loop_stop()