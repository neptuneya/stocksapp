import os
import yaml
import json
import requests

# Check for env variable PORT-- if it doesn't exist, just use 5000 as default
# This means you can export a different port before running this script if you have
# Flask running on a different port!
port = os.getenv("PORT", 5000)

# We add the port to our url prefix and store the url as a variable
# Note: We'll add the stock name to the end later in the script
our_api_url_prefix = f"http://localhost:{port}/stock/overview/"

# Read stocks_to_get.yaml to find out which stocks to hit
# Note: This will return us a dict {"stocks_to_check": ["stock1", "stock2", etc....]}
with open("stocks_to_get.yaml", "r") as file_to_read:
    stocks_to_get = yaml.safe_load(file_to_read)

for stock in stocks_to_get["stocks_to_check"]:
    full_url = our_api_url_prefix + stock
    api_response = requests.get(full_url)
    stock_info_for_today: bytes = (json.loads(api_response._content))["content"]
    print(f"STOCK NAME: {stock}")
    print(f"{json.dumps(stock_info_for_today)}")