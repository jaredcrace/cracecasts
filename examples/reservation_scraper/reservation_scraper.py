from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from icecream import ic

# Slack webhook URL
SLACK_WEBHOOK_URL = "<YOUR SLACK HOOK HERE"

def check_reservations():
    # Start Chrome WebDriver
    driver = webdriver.Chrome()

    # Navigate to the URL
    driver.get("https://www.misinewyork.com")

    # Wait until the element is clickable and then click it
    # Adjust the selector to match the actual button/link
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-brand-alt"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "seats"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//option[text()='2 People']"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "date"))
    ).send_keys("10/26/2023")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-brand"))
    ).click()

    # get the new iframe
    iframe_element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="Resy - Book Now"]')))
    driver.switch_to.frame(iframe_element)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "DropdownGroup__selector--date"))
    ).click()


    # find availability with 
    button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ResyCalendar-day.ResyCalendar-day--available.CalendarMonth__Cell.Button.Button--primary.Button--circle")))
    ic(button.text)

    # send to slack
    ic("send to slack")

    # Send to Slack
    slack_message = {
        'text': f'Available day is {button.text}.'
    }
    requests.post(SLACK_WEBHOOK_URL, json=slack_message)

    # Close the driver after scraping
    driver.quit()

if __name__ == "__main__":
    check_reservations()
