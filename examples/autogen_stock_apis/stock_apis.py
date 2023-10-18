import requests
from datetime import datetime

# API keys
FINNHUB_API_KEY = 'your_finnhub_api_key'
ALPHA_VANTAGE_API_KEY = 'your_alpha_vantage_api_key'
QUANDL_API_KEY = 'your_quandl_api_key'
IEX_CLOUD_API_KEY = 'your_iex_cloud_api_key'
TWELVE_DATA_API_KEY = 'your_twelve_data_api_key'

# Slack webhook URL
SLACK_WEBHOOK_URL = '<YOUR_SLACK_WEBHOOK_HERE>'

# Stock symbol
SYMBOL = 'F'

# Get today's date
today = datetime.today().strftime('%Y-%m-%d')

# Get stock price from Finnhub
finnhub_url = f'https://finnhub.io/api/v1/quote?symbol={SYMBOL}&token={FINNHUB_API_KEY}'
finnhub_response = requests.get(finnhub_url).json()
finnhub_price = finnhub_response['c']

# Get stock price from Alpha Vantage
alpha_vantage_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={ALPHA_VANTAGE_API_KEY}'
alpha_vantage_response = requests.get(alpha_vantage_url).json()

###################
# manually added 
###################
latest_date = next(iter(alpha_vantage_response['Time Series (Daily)']))

alpha_vantage_price = float(alpha_vantage_response['Time Series (Daily)'][latest_date]['4. close'])

# Get stock price from Quandl
quandl_url = f'https://www.quandl.com/api/v3/datasets/WIKI/{SYMBOL}/data.json?api_key={QUANDL_API_KEY}'
quandl_response = requests.get(quandl_url).json()
quandl_price = quandl_response['dataset_data']['data'][0][4]

# Get stock price from IEX Cloud
iex_cloud_url = f'https://cloud.iexapis.com/stable/stock/{SYMBOL}/quote?token={IEX_CLOUD_API_KEY}'
iex_cloud_response = requests.get(iex_cloud_url).json()
iex_cloud_price = iex_cloud_response['latestPrice']

# Get stock price from Twelve Data
twelve_data_url = f'https://api.twelvedata.com/time_series?symbol={SYMBOL}&interval=1day&apikey={TWELVE_DATA_API_KEY}'
twelve_data_response = requests.get(twelve_data_url).json()
twelve_data_price = float(twelve_data_response['values'][0]['close'])

# Compare prices
prices = {
    'Finnhub': finnhub_price,
    'Alpha Vantage': alpha_vantage_price,
    'Quandl': quandl_price,
    'IEX Cloud': iex_cloud_price,
    'Twelve Data': twelve_data_price
}
lowest_price_exchange = min(prices, key=prices.get)
lowest_price = prices[lowest_price_exchange]

print(prices)

# Print lowest price and exchange
print(f'The lowest price is {lowest_price} at {lowest_price_exchange}.')

# Send to Slack
slack_message = {
    'text': f'The lowest price is {lowest_price} at {lowest_price_exchange}.'
}
requests.post(SLACK_WEBHOOK_URL, json=slack_message)