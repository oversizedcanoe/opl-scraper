import datetime
from logger import logger
from mqtt import publish_mqtt
from scrape import Scraper
from settings import settings
    
if __name__ == "__main__":
    logger.log("Script started")

    scraper = Scraper()

    for user in settings.users:
        name = user['name']    
        barcode = user['barcode']    
        pin = user['pin']    

        logger.log("Scraping for " + name)

        books = scraper.scrape_opl(barcode, pin)
        update_time = datetime.datetime.now().isoformat()
        
        # Holds that aren't ready    
        holds = [book for book in books if (book.get("status") or "").lower() in ["not ready", "in transit"]]
        payload = {"count": len(holds), "items": holds, "last_updated": update_time }
        publish_mqtt(f"library/{name}/holds", payload)

        # Ready for pick up
        ready = [book for book in books if (book.get("status") or "").lower() == "ready"]
        payload = { "count": len(ready), "items": ready, "last_updated": update_time }
        publish_mqtt(f"library/{name}/ready", payload)

        # Checked out, not due
        checked_out = [book for book in books if (book.get("status") or "").lower() == "due later"]
        payload = { "count": len(checked_out), "items": checked_out, "last_updated": update_time }
        publish_mqtt(f"library/{name}/checked_out", payload)

        # Checked out, due now
        due = [book for book in books if (book.get("status") or "").lower() == "overdue"]
        payload = { "count": len(due), "items": due, "last_updated": update_time }
        publish_mqtt(f"library/{name}/due", payload)

    logger.log("Done scraping")

    scraper.dispose()
