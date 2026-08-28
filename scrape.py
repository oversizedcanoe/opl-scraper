import json
import os
import re
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_opl() -> list:
    BARCODE = os.getenv("OPL_BARCODE")
    PIN = os.getenv("OPL_PIN")

    options = webdriver.ChromeOptions()
    if sys.platform == 'win32':
        print('Running headed mode')
        driver = webdriver.Chrome(options=options)
    else:
        # is linux, run headless and set executable location        
        options.add_argument("--headless=new") 
        options.add_argument("--no-sandbox") 
        service = Service(executable_path='/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://forms.biblioottawalibrary.ca/en/oplusers/login")
    
    # Wait for elements and populate
    wait = WebDriverWait(driver, 10)
    
    user_input = wait.until(EC.presence_of_element_located((By.ID, "user_name")))
    pin_input = driver.find_element(By.ID, "user_pin")
    login_button = driver.find_element(By.ID, "edit-commit")
    
    user_input.send_keys(BARCODE)
    pin_input.send_keys(PIN)
    
    login_button.click()
    
    #  Wait for redirect to complete
    wait.until(EC.url_changes("https://forms.biblioottawalibrary.ca/en/oplusers/login"))
    
    # Navigate to holds page
    driver.get("https://ottawa.bibliocommons.com/v2/holds")
    wait.until(EC.url_contains("/holds"))

    # Parse books that are ready
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cp-batch-actions-list-item")))

    items = driver.find_elements(By.CLASS_NAME, "cp-batch-actions-list-item")

    # Helper function to safely extract text without crashing if an element is missing
    def get_text(parent, find_by, css_selector):
        try:
            return parent.find_element(find_by, css_selector).text.strip()
        except:
            return None

    books = []
    for item in items:
        queue_text = get_text(item, By.CLASS_NAME, 'cp-hold-position') or ''
        queue_match = re.search(r'#\s*(\d+)\s+on\s+(\d+)', queue_text.replace('\n', ' '))
        
        books.append({
            'title': get_text(item, By.CLASS_NAME, 'title-content'),
            'author': get_text(item, By.CLASS_NAME, 'author-link'),
            'format': get_text(item, By.CLASS_NAME, 'display-info-primary'),
            'status': get_text(item, By.CLASS_NAME, 'status-name'),
            'queuePosition': queue_match.group(1) if queue_match else None,
            'totalCopies': queue_match.group(2) if queue_match else None,
            'pickupLocation': get_text(item, By.CSS_SELECTOR, '.holds-pickup-dropdown .selected-value') or get_text(item, By.CLASS_NAME, 'branch-name'),
            'placedOn': get_text(item, By.CSS_SELECTOR, '.cp-holds-placed-date .cp-short-formatted-date'),
            'expiry': get_text(item, By.CSS_SELECTOR, '.cp-holds-expire-date .cp-short-formatted-date') or get_text(item, By.CSS_SELECTOR, '.cp-pick-up-date .cp-short-formatted-date')
        })

    # Navigate to checkedout page
    driver.get("https://ottawa.bibliocommons.com/v2/checkedout")
    wait.until(EC.url_contains("/checkedout"))

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cp-batch-actions-list-item")))

    items = driver.find_elements(By.CLASS_NAME, "cp-batch-actions-list-item")

    for item in items:
        books.append({
            'title': get_text(item, By.CLASS_NAME, 'title-content'),
            'author': get_text(item, By.CLASS_NAME, 'author-link'),
            'format': get_text(item, By.CLASS_NAME, 'display-info-primary'),
            'status': get_text(item, By.CLASS_NAME, 'status-name'),
            'dueDate': get_text(item, By.CLASS_NAME, 'cp-short-formatted-date'),
        })

    # Eventually implement "Saved for later" list too
    
    # # Navigate to the for later page
    # driver.get("https://ottawa.bibliocommons.com/collection/show/my/library/for_later")
    # wait.until(EC.url_contains("/for_later"))

    # # Can see title author format, plus status (Available, All Copies in use (no queue), added date)

    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cp-batch-actions-list-item")))

    # items = driver.find_elements(By.CLASS_NAME, "cp-batch-actions-list-item")

    # for item in items:
    #     books.append({
    #         'title': get_text(item, By.CLASS_NAME, 'title-content'),
    #         'author': get_text(item, By.CLASS_NAME, 'author-link'),
    #         'format': get_text(item, By.CLASS_NAME, 'display-info-primary'),
    #         'status': get_text(item, By.CLASS_NAME, 'status-name'),
    #         'dueDate': get_text(item, By.CLASS_NAME, 'cp-short-formatted-date'),
    #     })

    return books