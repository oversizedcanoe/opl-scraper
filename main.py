import datetime
import os
from dotenv import load_dotenv
from scrape import scrape_opl
from mqtt import publish_mqtt
    
if __name__ == "__main__":
    load_dotenv()

    NAME = os.getenv("NAME")

    books = scrape_opl()

    update_time = datetime.datetime.now().isoformat()
    
    # Holds that aren't ready    
    holds = [book for book in books if book.get("status", "").lower() in ["not ready", "in transit"]]
    payload = {"count": len(holds), "items": holds, "last_updated": update_time }
    publish_mqtt(f"library/{NAME}/holds", payload)

    # Ready for pick up
    ready = [book for book in books if book.get("status", "").lower() == "ready"]
    payload = { "count": len(ready), "items": ready, "last_updated": update_time }
    publish_mqtt(f"library/{NAME}/ready", payload)

    # Checked out, not due
    checked_out = [book for book in books if book.get("status", "").lower() == "due later"]
    payload = { "count": len(checked_out), "items": checked_out, "last_updated": update_time }
    publish_mqtt(f"library/{NAME}/checked_out", payload)

    # Checked out, due now
    due = [book for book in books if book.get("status", "").lower() == "???"]
    payload = { "count": len(due), "items": due, "last_updated": update_time }
    publish_mqtt(f"library/{NAME}/due", payload)
