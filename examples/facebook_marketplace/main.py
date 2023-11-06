from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import smtplib
from email.message import EmailMessage
import dotenv
from icecream import ic

dotenv.load_dotenv()

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
        smtp.login(EMAIL, os.environ.get("google_token"))
        smtp.send_message(msg)

    ic("Email sent!")

# This is the port you started Chrome with for remote debugging.
debugging_port = 9222

# Setup Selenium to connect to the remote Chrome
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", f"localhost:{debugging_port}")

# Path to your ChromeDriver executable
chrome_driver_path = "<YOUR DRIVER PATH>"

service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Now you can interact with the existing browser session
url = "https://www.facebook.com/marketplace/houston/search?minPrice=2000&maxPrice=3000&query=trucks&exact=false"
ic(url)
driver.get(url)
ic(driver.title)

image_path = "logs/pic1.png"
ic(image_path)
driver.save_screenshot(image_path)

# send the pic via email
send_email("test subject", "test body message", image_path)

driver.quit()  

