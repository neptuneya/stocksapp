from io import BytesIO
import json

import requests
import pandas
from flask import Response

def get_general_stock_info(symbol):
    """Get stock info for provided shorthand symbol"""

    # Construct the URL to use whatever shorthand stock symbol-- I tested this in a browser
    # Something like GOOG, AMD, GME, etc...
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?interval=1d&events=history&includeAdjustedClose=true"
    
    # Random bullshit headers to get the request to pass
    headers = headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    # Make a HTTP GET request to the yahoo news url and return a Response object
    yahoo_response = requests.get(url, headers=headers)

    # Use pandas.read_csv to read the CSV content returned by yahoo
    # Since the csv returned by yahoo is actually "bytes" datatype, use BytesIO()
    # To cast it to a readable string so pandas.read_csv can actually read it
    content_as_dataframe = pandas.read_csv(BytesIO(yahoo_response.content), engine="python")

    # Use pandas .to_json() method to convert the dataframe to json in one line
    # Remember: Our API can't return a dataframe-- it would error if we tried
    # So we must convert to json so we can return the data to our user
    raw_json_content = content_as_dataframe.to_json(orient="records", lines=True)

    # We still have to parse the raw_json_content to remove backslashes
    # Or else, it looks like this: "content": "\"[{\\\"Date\\\":\\\"2023-06-02\\\"....}
    parsed_json_content = json.loads(raw_json_content)

    # Create a flask Response object that can be returned by the endpoint
    # Note: flask API can only return certain data types, like json or flask Response objects
    response = Response()

    # Make our API return the HTTP status that yahoo gave us
    # If Yahoo shit the bed on us, we want our API to tell the user
    # by passing alone the same HTTP status code (e.g. 404 Not Found, 500 Internal Server Error)
    response.status_code = yahoo_response.status_code
    
    # Add content to our response that our API will return
    # We are using json.dumps() so that the json data will look nice and readable
    response._content = parsed_json_content
    
    return response