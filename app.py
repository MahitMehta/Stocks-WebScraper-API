from selenium import webdriver
from flask import Flask, render_template


def get_stock_price():
    url = 'https://www.google.com/finance/quote/DMTK:NASDAQ'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    broswer = webdriver.Chrome('./chromedriver.exe', options=options)
    broswer.get(url)

    stock_price = broswer.find_element_by_xpath(
        '//*[@id="yDmH0d"]/c-wiz/div/div[3]/main/div[2]/c-wiz/div/div[1]/div[1]/div/div[1]/div[1]/div/div[1]/div/span/div/div').text

    return stock_price


app = Flask(__name__)


@app.route("/", methods=["GET"])
def route_directory():
    stock_price = get_stock_price()
    return render_template("index.html", stock_price=stock_price)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
