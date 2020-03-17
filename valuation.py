# API to interface with https://financialmodelingprep.com/developer/docs/

from urllib.request import urlopen
from urllib.parse import urljoin
import json
import argparse

class FinanceModelingPrep:
    

    def __init__(self):
        self.url_base = "https://financialmodelingprep.com/api/v3/"

    def get_data(self, url):
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)

    def get_profile(self, ticker):
        url = urljoin(self.url_base, "company/profile/" +  ticker)
        data = self.get_data(url)
        return data

    def get_quote(self, ticker):
        url = urljoin(self.url_base, "quote/" + ticker)
        data = self.get_data(url)
        return data

    def get_annual_financials(self, ticker):
        """This can get batch data, comma seperated list of tickers"""
        url = urljoin(self.url_base, "financials/income-statement/" + ticker)
        data = self.get_data(url)
        return data
    
    def get_annual_balance_sheet(self, ticker):
        url = urljoin(self.url_base, "financials/balance-sheet-statement/" + ticker)
        data = self.get_data(url)
        return data
    
    def get_cash_flow(self, ticker):
        url = urljoin(self.url_base, "financials/cash-flow-statement/" + ticker)
        data = self.get_data(url)
        return data
    
    def get_ratios(self, ticker):
        url = urljoin(self.url_base, "financial-ratios/" + ticker)
        data = self.get_data(url)
        return data
    
    def get_key_metrics(self, ticker):
        url = urljoin(self.url_base, "company-key-metrics/" + ticker)
        data = self.get_data(url)
        return data

    def get_rating(self, ticker):
        url = urljoin(self.url_base, "company/rating/" + ticker)
        data = self.get_data(url)
        return data
    
    def get_growth(self, ticker):
        url = urljoin(self.url_base, "financial-statement-growth/" + ticker)
        data = self.get_data(url)
        return data

    def get_real_time_price(self, ticker):
        """Can get batch data"""
        url = urljoin(self.url_base, "real-time-price/", ticker)
        data = self.get_data(url)
    
    def form_ticker_string(self, tickers):
        """Form a comma seperate list of tickers. Then can be appended to the URL"""
        ticker_string = ""
        for ticker in tickers:
            ticker_string = ticker_string + ticker + ","

        return ticker_string

    def get_valuation(self, ticker):
        # get all the required data
        financial_data = self.get_annual_financials(ticker)
        growth_data = self.get_growth(ticker)
        quote_data = self.get_quote(ticker)

        # extract out the data we need
        eps = float(financial_data['financials'][0]['EPS'])
        eps_growth = float(growth_data['growth'][0]['EPS Growth'])
        price = float(quote_data[0]['price'])

        # compute valuation
        value_graham = eps * (8.5 + 2 * eps_growth)
        print("{:<8s} {:<8.2f} {:<8.2f} {:<8.2f}".format(ticker,price, value_graham, price/value_graham))
        # return estimate value
        return (price, value_graham)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("ticker", help="Stock ticker symbol", nargs="*", default=["AAPL"])
    args = parser.parse_args()

    fmp = FinanceModelingPrep()
   
    tickers = args.ticker
    print("{:<8s} {:<8s} {:<8s} {:<8s}".format("Ticker", "Price", "Value", "P/V Ratio"))
    for ticker in tickers:
        valuation = fmp.get_valuation(ticker)
