# opl-scraper
Scrapes the Ottawa Public Library for books that are checked out, on hold, due, and on hold.
Publishes the results with MQTT to a configurable server address.

# Output
The application publishes JSON via MQTT to the URL/port configured in the .env file, with the following endpoints:
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
2. Create a `.env` file with your OPL credentials, using `EXAMPLE.env` as a template.

    ```text
    OPL_BARCODE=00000000000000
    OPL_PIN=0000
    HOSTNAME=homeassistant.local
    PORT=1883
    NAME=Bob
    MQTT_USER=USER
    MQTT_PASS=PASS
    ```

3. Create the Python venv: `python3 -m venv venv` (`deactivate` to end the venv)

4. Start the venv
Linux: `source venv/bin/activate`
Windows: `.\venv\Scripts\activate`

5. Install dependencies: `pip install -r requirements.txt`

### To run locally for debugging
1. Run the scraper: `python3 main.py`.

Options:

- `-v` or `--verbose` for verbose mode
- `-h` or `--headed` for headed mode (browser popup)

>Note: if running on Linux, you must install Chromium Driver with:
>
>`sudo apt install -y chromium chromium-driver`

### To deploy with systemd
1. Create a service file, using `EXAMPLE-library-script.service` as a template.

`sudo nano /etc/systemd/system/library-script.service`

```
[Unit]
Description=Library Scraper
Wants=library-script.service
[Service]
ExecStart=/REPO_PATH/venv/bin/python3 /REPO_PATH/main.py
User=LINUX_USER
[Install]
WantedBy=library.target
```

2. Create a timer file, using `EXAMPLE-library-script.timer` as a template.

`sudo nano /etc/systemd/system/library-script.timer`
```
[Unit]
Description=Run library script every 30 mins 9am-8pm

[Timer]
Unit=library-script.service
OnCalendar=*-*-* 09..20:00,30:00
Persistent=true

[Install]
WantedBy=timers.target
```

3. Start Timer
`sudo systemctl daemon-reload`
`sudo systemctl enable --now library-script.timer`

4. View Status to confirm it is active/waiting

`sudo systemctl status library-script.timer`

5. If changes need to be made to files or systemd files, after changing:
`sudo systemctl daemon-reload`
`sudo systemctl restart library-script.timer`

