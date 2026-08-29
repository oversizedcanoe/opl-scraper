# opl-scraper
Scrapes the Ottawa Public Library for books that are checked out, on hold, due, and on hold.
Publishes the results with MQTT to a configurable server address.

# Output
The application publish JSON via MQTT to the URL/port configured in the .env file, with the following endpoints:
 - `library/{NAME}/holds`
 - `library/{NAME}/ready`
 - `library/{NAME}/checked_out`
 - `library/{NAME}/due`

The output will be in the following format:

```json
{
  "count": 1,
  "items": [
    {
      "title": "My Book Name",
      "author": "Author Name",
      "format": "Book, 1975",
      "status": "Due later",
      "dueDate": "Jan 01, 2099"
    }
  ],
  "last_updated": "2026-08-28T21:28:21.446134"
}

```

# How To

1. Clone the repo and `cd` into it.
2. Create an `.env` file with your OPL credentials, using `sample.env` as a template.

    ```text
    OPL_BARCODE=00000000000000
    OPL_PIN=0000
    NAME=Bob
    MQTT_USER=USER
    MQTT_PASS=PASS
    ```

3. Create the Python venv: `python -m venv venv`

> Note: Substitute `python` for `python3` depending on your setup.

4. Start the venv
Linux: `source venv/bin/activate`
Windows: `.\venv\Scripts\activate`

5. Install dependencies: `pip install -r requirements.txt`

### To run locally for debugging
1. Run the scraper: `python main.py`.

Options:

- `-v` or `--verbose` for verbose mode
- `-h` or `--headed` for headed mode (browser popup)

>Note: if running on Linux, you must install Chromium Driver with:
>
>`sudo apt install -y chromium chromium-driver`

### To deploy with systemd
