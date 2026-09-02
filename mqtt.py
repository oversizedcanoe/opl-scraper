import json
import paho.mqtt.publish as publish
from logger import logger
from settings import settings


def publish_mqtt(endpoint, data):
    payload = json.dumps(data)

    publish.single(
        endpoint,
        payload=payload,
        hostname=settings.hostname,
        port=settings.port,
        auth={'username': settings.mqtt_user, 'password': settings.mqtt_user}
    )

    path = f"mqtt://{settings.mqtt_user}:***@{settings.hostname}:{settings.port}/{endpoint}"
    logger.log('Published the following payload to ' + path)
    logger.log(payload)