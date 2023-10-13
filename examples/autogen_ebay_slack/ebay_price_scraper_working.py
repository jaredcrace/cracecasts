# filename: ebay_price_scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

def send_to_slack(text):
    webhook_url = '<YOUR_SLACK_WEBHOOK_HERE>' 
    slack_data = {'text': text}
    response = requests.post(
        webhook_url, json=slack_data,
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

driver = webdriver.Chrome()  # or webdriver.Chrome(), depending on your browser

driver.get("https://www.ebay.com")

search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "gh-ac"))
)
search_box.send_keys("iphone 14")
search_box.submit()

time.sleep(5)  # wait for the page to load

prices = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "s-item__price"))
)

for price in prices:
    price_text = price.text
    if len(price_text) > 1:
        print(price_text)
        send_to_slack(price_text)

driver.quit()