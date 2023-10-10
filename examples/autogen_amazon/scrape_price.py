# filename: scrape_price.py

import requests
from bs4 import BeautifulSoup

def get_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        price = soup.find("span", attrs={'class':'a-offscreen'}).string
    except AttributeError:
        price = "Could not find the price. The HTML structure of the page might be different from what the script expects."

    return price

url = 'http://example.com/product-page'
print(get_price(url))