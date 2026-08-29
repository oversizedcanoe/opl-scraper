import os
import paho.mqtt.publish as publish
import json

def publish_mqtt(endpoint, data):
    MQTT_USER = os.getenv("MQTT_USER")
    MQTT_PASS = os.getenv("MQTT_PASS")

    payload = json.dumps(data)

    publish.single(
        endpoint,
        payload=payload,
        hostname="homeassistant.local",
        port=1883,
        auth={'username': MQTT_USER, 'password': MQTT_PASS}
    )

    # print('Published the following payload to: ' + endpoint)
    # print(payload)