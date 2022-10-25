from datetime import datetime
from datetime import date
import yfinance as yf
from flask import Flask
from flask import render_template
from flask import request
import pytz

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':

        current_time = datetime.now().ctime()
        ticker_symbol = request.form.get("ticker_symbol")
        company_info = yf.Ticker(ticker_symbol)

    if company_info.history(period="max").empty is False:

        company_name = company_info.info['longName'] + ' (' + ticker_symbol.upper() + ')'
        last_two_days_data = round(company_info.history(period='2d'), 2)
        previous_price = last_two_days_data['Close'][0]
        todays_price = last_two_days_data['Close'][1]
        value_change = round(todays_price - previous_price, 2)
        percentage_change = round((value_change / previous_price) * 100, 2)

        if(value_change > 0):
            value_change = '+' + str(value_change)

        if(percentage_change > 0):
            percentage_change = '+' + str(percentage_change)

        todays_price = "$" + str(todays_price)
        value_change = "$" + str(value_change)
        percentage_change = "(" + str(percentage_change) + "%)"

        stock_data = {
            "current_time": current_time, 
            "company_name": company_name,
            "todays_price": todays_price,
            "value_change": value_change, 
            "percentage_change": percentage_change, 
            "error": ""
        }
        return render_template("index.html", **stock_data)

    else:
        stock_data = {"error":"YOU HAVE ENTERED WRONG TICKER SYMBOL"}
        return render_template("index.html", **stock_data)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, Host='0.0.0.0')
