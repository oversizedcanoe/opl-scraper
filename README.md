# opl-scraper

Scrapes the Ottawa Public Library for books that are checked out, on hold, due, and on hold.

This application will run headless (no browser) on Linux and headed (browser pops up) on Windows.

# How To

1. Clone the repo and `cd` into it.
2. Create an `.env` file with your OPL credentials:

    ```text
    OPL_BARCODE=00000000000000
    OPL_PIN=0000
    NAME=Bob
    MQTT_USER=USER
    MQTT_PASS=PASS
    ```

3. Create the Python venv: `python -m venv venv`
4. Start the venv: `.\venv\Scripts\activate`
5. Install dependencies: `pip install -r requirements.txt`

### To run locally for debugging
1. Run the scraper: `python main.py`

### To deploy with systemd
Note: if running on Linux, you must install Chromium Driver:
`sudo apt install chromium-chromedriver`
