import requests
from io import BytesIO
from http import HTTPStatus
from pandas import pandas
from flask import Response

def get_general_stock_info(symbol):
    """Get stock info for provided shorthand symbol"""
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?interval=1d&events=history&includeAdjustedClose=true"
    # Random bullshit headers to get the request to pass
    headers = headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    raw_data = requests.get(url, headers=headers)
    content = pandas.read_csv(BytesIO(raw_data.content), engine="python")
    resp = Response()
    resp.status_code = HTTPStatus.OK
    resp._content = content.to_json()
    return resp