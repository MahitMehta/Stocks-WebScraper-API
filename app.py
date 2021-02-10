from selenium import webdriver
from flask import Flask
from flask import request
import os
import json

options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
broswer = webdriver.Chrome("./chromedriver.exe", options=options)


def get_stock_price(ticker, stock_exchange):
    try:
        url = f'https://www.google.com/finance/quote/{ticker}:{stock_exchange}'
        broswer.get(url)
        stock_price = broswer.find_element_by_xpath(
            '//*[@id="yDmH0d"]/c-wiz/div/div[3]/main/div[2]/c-wiz/div/div[1]/div[1]/div/div[1]/div[1]/div/div[1]/div/span/div/div').text
        return stock_price
    except Exception:
        return None


def error_handler():
    err_msg = "Please provide a valid ticker and stock_exchange parameter"
    err = {"error": err_msg}
    json_err = json.dumps(err)
    return json_err


app = Flask(__name__)


@ app.route("/", methods=["GET"])
def route_directory():
    req = request.args
    ticker = req.get("ticker")
    stock_exchange = req.get("stock_exchange")

    if not ticker or not stock_exchange:
        return error_handler()

    current_price = get_stock_price(
        ticker=ticker, stock_exchange=stock_exchange)

    if not current_price:
        return error_handler()

    data = {
        "ticker": ticker,
        "stock_exchange": stock_exchange,
        "current_price": current_price
    }
    json_data = json.dumps(data)

    return json_data


if __name__ == "__main__":
    app.run(debug=True, port=5000)
