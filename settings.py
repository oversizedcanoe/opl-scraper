import json

class Settings:
    def __init__(self):
        with open("config.json", "r") as f:
            config = json.load(f)
            self.hostname = config['hostname']
            self.port = config['port']
            self.mqtt_user = config['mqtt_user']
            self.mqtt_pass = config['mqtt_pass']
            self.headless = config['headless']
            self.logging = config['logging']
            self.users = config['users']

settings = Settings()