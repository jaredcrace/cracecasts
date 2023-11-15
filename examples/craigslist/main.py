'''
Notes:
pip install python-dotenv icecream selenium
pip install openai==0.28
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import dotenv
from icecream import ic
import smtplib
from email.message import EmailMessage
import openai
import time

dotenv.load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

def engage_ai(listing_data):
    system_message = f"""
    You are an expert in finding and compairing good vehicle deals on craigslist.
    """

    user_message = f"""
    Given a set of vehicle listings on craigslist, your job is to give your opinon of which 
    deal is best. You are to give your reasonings and feel free to reference other listings
    as your justitification.  

    Listings data 
    {listing_data}
    """

    messages=[
        {"role": "system", "content": f"{system_message}"},
        {"role": "user", "content": f"{user_message}"},
        ]

    ic(f"calling openai with prompt: {user_message}")
    ans = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=2048,
        messages=messages,
    )

    res = ans["choices"][0]["message"]["content"]
    ic(res)

    return res


def send_email(msg_subject, msg_body):
    EMAIL = "<YOUR EMAIL>"
    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = msg_subject 
    msg['From'] = EMAIL 
    msg['To'] = EMAIL 
    msg.set_content(msg_body)

    ic(msg)
    # Connect to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL, os.environ.get("GOOGLE_TOKEN"))
        smtp.send_message(msg)

    ic("Email sent!")

if __name__ == "__main__":
    # Start Chrome WebDriver
    driver = webdriver.Chrome()

    city = "houston"
    min_price = "3000"
    max_price = "4000"
    url = f"https://{city}.craigslist.org/search/cto?min_price={min_price}&max_price={max_price}"

    # Navigate to the URL
    ic(url)
    driver.get(url)

    time.sleep(5)

    # page-1 returned 120 listings
    page = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "search-results-page-1")))
    listing_data = page.text.split("\n")
    ic(listing_data)

    # cap the amount listings to 50 vehicles
    listing_data = listing_data[0:200]
    ic(len(listing_data))

    # send to the AI
    chatgpt_res = engage_ai(listing_data)
    ic(chatgpt_res)

    # send email with png
    send_email("craigslist update", chatgpt_res)

    driver.quit() 