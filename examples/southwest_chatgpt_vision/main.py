'''
Notes:
pip install python-dotenv icecream requests selenium
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import base64
import dotenv
import requests
from icecream import ic
import json
import smtplib
from email.message import EmailMessage

dotenv.load_dotenv()

def ask_chatgpt(image_path):
    api_key = os.environ.get("OPENAI_API_KEY") 

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    PROMPT = """
        Is there a flight that is cheaper than $150? Follow these instructions:
        If answer is yes, respond with: "YES" and then provide the flight times and price.
        If answer is no, respond with: "NO".  
    """

    ic(PROMPT)
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": PROMPT 
              },
              {
                "type": "image_url",
                "image_url": {
                  "url": f"data:image/png;base64,{base64_image}"
                }
              }
            ]
          }
        ],
        "max_tokens": 300
    }

    ic("asking chatgpt")
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    res = response.json()
    ic(res)
    return res['choices'][0]['message']['content']

def send_email(msg_subject, msg_body, image_path):
    EMAIL = "<YOUR EMAIL>"
    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = msg_subject 
    msg['From'] = EMAIL 
    msg['To'] = EMAIL 
    msg.set_content(msg_body)

    # add the png
    with open(image_path, 'rb') as img:
        # Know your content-type
        msg.add_attachment(img.read(), maintype="image", subtype="png", filename=image_path)

    ic(msg)
    # Connect to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL, os.environ.get("GOOGLE_TOKEN"))
        smtp.send_message(msg)

    ic("Email sent!")

if __name__ == "__main__":
    # Start Chrome WebDriver
    driver = webdriver.Chrome()

    # Navigate to the URL
    url = ("https://www.southwest.com/air/booking/select.html?int=HOMEQBOMAIR&adultPassengersCount=1&departureDate="
            "2023-12-01&destinationAirportCode=DEN&fareType=USD&originationAirportCode=LAX&passengerType=ADULT&promoCode="
            "&returnDate=2023-12-10&tripType=roundtrip&from=LAX&to=DEN&adultsCount=1&departureTimeOfDay=ALL_DAY&"
            "reset=true&returnTimeOfDay=ALL_DAY")
    ic(url)
    driver.get(url)

    # Assuming there's a button or link to click to show reservations
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "form-mixin--submit-button"))).click()

    # Wait for page to load 
    time.sleep(5)

    # save screenshot
    image_path = "logs/flight_info1.png"
    driver.save_screenshot(image_path)

    # send to the AI
    chatgpt_res = ask_chatgpt(image_path)
    ic(chatgpt_res)

    if 'NO' in chatgpt_res:
        ic("No flights at that cost")
        exit()

    # send email with png
    send_email("flight bot", chatgpt_res, image_path)
    