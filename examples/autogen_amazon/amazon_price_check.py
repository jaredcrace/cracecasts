# filename: amazon_price_check.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Go to Amazon
driver.get("https://www.amazon.com")

# Find the search box, enter "iPhone 13", and search
search_box = driver.find_element(By.ID, "twotabsearchtextbox")
search_box.send_keys("iPhone 13")
search_box.send_keys(Keys.RETURN)

# Wait for the page to load
time.sleep(3)

# Find the price of the first result
price = driver.find_element(By.CSS_SELECTOR, ".a-price-whole").text

# Print the price
print("The price of the iPhone 13 on Amazon is: $" + price)

# Close the driver
driver.quit()