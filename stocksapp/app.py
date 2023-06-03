from http import HTTPStatus
from flask import Flask, request
from .stocks import get_general_stock_info

app = Flask(__name__)

@app.route('/health', methods=["GET"])
def health_check():
    return {"status": HTTPStatus.OK}

@app.route('/stock/overview/<symbol>')
def get_stock_overview(symbol):
    response = get_general_stock_info(symbol)
    return {"status": response.status_code, "content": response._content}