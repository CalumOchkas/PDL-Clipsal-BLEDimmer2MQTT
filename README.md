Allows you to control your PDL or Clipsal BLE Dimmer with MQTT for use with HomeAssistant

# Requirements

* Python 3.6+
* paho-mqtt
* bluez
* Bluetooth 5.0+ _(see notes)_

## RaspberryPi 4

This has been tested on a RaspberryPi 4 with the full install of PiOS. As per [this comment](https://github.com/nathankellenicki/node-poweredup/issues/110#issuecomment-710113065), BlueZ needs to be downgraded to successfully pair the device with the dimmer. To downgrade, run the following lines:
```
wget http://archive.raspberrypi.org/debian/pool/main/b/bluez-firmware/bluez-firmware_1.2-4+rpt2_all.deb
sudo dpkg -i bluez-firmware_1.2-4+rpt2_all.deb
```

## Bluetooth 5.0

From initial testing, there has only been successful pairing with the dimmers from devices with at least Bluetooth 5.0. There is however no requirement for BT5. from mobile devices. Your mileage may vary.

## Paired controller/dimmer

The controller must already be paired with the dimmer. This step is seperate as it's easier to troubleshoot outside of the script, and only needs to happen once. Run the following commands within `bluetoothctl` from your controller:

```
power on
agent on
default-agent
scan on
```

Then, with the MAC address it returns for the dimmer:
```
scan off
trust XX:XX:XX:XX:CH:28
pair XX:XX:XX:XX:CH:28
```
If at any point there are errors, troubleshoot this before continuing.

The total output should look as follows:
```
[bluetooth]# power on
Changing power on succeeded
[bluetooth]# agent on
Agent is already registered
[bluetooth]# default-agent
Default agent request successful
[bluetooth]# scan on
Discovery started
[CHG] Controller YY:YY:YY:YY:D9:F9 Discovering: yes
... <other devices>
[NEW] Device XX:XX:XX:XX:C3:E0 CH-DIMMER_C3E0
... <other devices>
[bluetooth]# scan off
Discovery stopped
[bluetooth]# trust XX:XX:XX:XX:C3:E0
[CHG] Device XX:XX:XX:XX:C3:E0 Trusted: yes
Changing XX:XX:XX:XX:C3:E0 trust succeeded
[bluetooth]# pair XX:XX:XX:XX:C3:E0
Attempting to pair with XX:XX:XX:XX:C3:E0
[CHG] Device XX:XX:XX:XX:C3:E0 Connected: yes
[CHG] Device XX:XX:XX:XX:C3:E0 UUIDs: 00001800-0000-1000-8000-00805f9b34fb
[CHG] Device XX:XX:XX:XX:C3:E0 UUIDs: 0000180a-0000-1000-8000-00805f9b34fb
[CHG] Device XX:XX:XX:XX:C3:E0 UUIDs: 1d14d6ee-fd63-4fa1-bfa4-8f47b42119f0
[CHG] Device XX:XX:XX:XX:C3:E0 UUIDs: 720a7080-9c7d-11e5-a7e3-0002a5d5c51b
[CHG] Device XX:XX:XX:XX:C3:E0 UUIDs: 720a9080-9c7d-11e5-a7e3-0002a5d5c51b
[CHG] Device XX:XX:XX:XX:C3:E0 ServicesResolved: yes
[CHG] Device XX:XX:XX:XX:C3:E0 Paired: yes
```


# Setup

## Parameters

* `dimmerAddress`: Mac address of dimmer
* `mqttBroker`: MQTT Broker Address
* `mqttPort`: MQTT Broker Port
* `room`: Name of room with light, used for topics
* __Topics__: The topics are set to match the home assistant configuration below

## Parameters

1. Ensure the requirements are met above
2. Pair your bluetooth controller to the BLE dimmer
3. Run `python3 main.py` from the script directory


## HomeAssistant Configuration

Utilize the [MQTT-Light HomeAssistant Integration](https://www.home-assistant.io/integrations/light.mqtt) with the config YAML as follows (you will need to change the topics from `bedroom` to whichever room you have configured in `main.py`)

```
light:
  - platform: mqtt
    name: "Bedroom Light"
    unique_id: bedroomlight
    state_topic: "bedroom/light/status"
    command_topic: "bedroom/light/switch"
    brightness_state_topic: 'bedroom/light/brightness'
    brightness_command_topic: 'bedroom/light/brightness/set'
    brightness_scale: 10000
    qos: 0
    payload_on: "ON"
    payload_off: "OFF"
    optimistic: false
```

# Thanks
Many thanks for others that helped give me the assistance to put this together [here](https://github.com/kenhuang/docker-homebridge/issues/1)