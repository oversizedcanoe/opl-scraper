import os
import paho.mqtt.publish as publish
import json
import sys

def publish_mqtt(endpoint, data):
    HOSTNAME = os.getenv("HOSTNAME")
    PORT = int(os.getenv("PORT"))
    MQTT_USER = os.getenv("MQTT_USER")
    MQTT_PASS = os.getenv("MQTT_PASS")

    payload = json.dumps(data)

    publish.single(
        endpoint,
        payload=payload,
        hostname=HOSTNAME,
        port=PORT,
        auth={'username': MQTT_USER, 'password': MQTT_PASS}
    )

    verbose = any(arg in sys.argv for arg in ('-v', '--verbose'))

    if verbose:
        path = f"mqtt://{MQTT_USER}:***@{HOSTNAME}:{PORT}/{endpoint}"
        print('Published the following payload to ' + path)
        print(payload)