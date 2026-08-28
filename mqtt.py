import os
import paho.mqtt.publish as publish
import json

def publish_mqtt(endpoint, data):
    MQTT_USER = os.getenv("MQTT_USER")
    MQTT_PASS = os.getenv("MQTT_PASS")

    publish.single(
        endpoint,
        payload=json.dumps(data),
        hostname="homeassistant.local",
        port=1883,
        auth={'username': MQTT_USER, 'password': MQTT_PASS}
    )