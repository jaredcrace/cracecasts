# filename: airbnb_search.py

import requests
from bs4 import BeautifulSoup

# Step 1: Go to Airbnb
url = "https://www.airbnb.com/"

# Step 2: Search for an Austin Texas stay from Oct 10, 2023 - Oct 11, 2023
search_params = {
    "location": "Austin, Texas",
    "checkin": "2023-10-10",
    "checkout": "2023-10-11"
}

response = requests.get(url, params=search_params)
response.raise_for_status()

# Step 3: Gather the results
soup = BeautifulSoup(response.content, "html.parser")
results = soup.find_all("div", class_="c4mnd7m dir dir-ltr")[:10]

# Step 4: Print the results
for result in results:
    print(result.get_text())