import datetime
from settings import settings

class Logger:
    def __init__(self):
        pass

    def log(self, message):
        if settings.logging:
            print(f"{datetime.datetime.now()} - {message}")        

logger = Logger()