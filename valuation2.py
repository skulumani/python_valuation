#!/usr/bin/env python3
# API to interface with https://financialmodelingprep.com/developer/docs/

from urllib.request import urlopen
from urllib.parse import urljoin
import json
import argparse
import csv

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

    def get_stock_data(self, tickers):
        """Single function to get all the data and store as member variables"""
        self.financial_data = self.get_annual_financials(ticker)
        self.growth_data = self.get_growth(ticker)
        self.quote_data = self.get_quote(ticker)


    def get_valuation(self, ticker):
        # extract out the data we need
        eps = float(self.financial_data['financials'][0]['EPS'])
        eps_growth = float(self.growth_data['growth'][0]['5Y Net Income Growth (per Share)'])
        price = float(self.quote_data[0]['price'])
       
        # compute graham valuation
        value_graham = eps * (8.5 + 2 * eps_growth*100)
        value_exp = eps * 12 * (1 + eps_growth)**5
        # return estimate value
    
        # compute exponential growth valuation
        print("{:<16s} {:<16.2f} {:<16.2f} {:<16.2f} {:<16.2f}".format(ticker,
                                                                  price,
                                                                  value_exp, 
                                                                  value_graham, 
                                                                  price/value_exp))
        # return estimate value
        return (price, value_exp, value_graham)
#   """Writes stock data to CSV"""
    def write_to_csv(self, ticker):
        with open("Stock Data Output.csv", mode = "a", newline = '\n') as Output:
            csv_writer = csv.writer(Output, delimiter = ',')
            eps = float(self.financial_data['financials'][0]['EPS'])
            eps_growth = float(self.growth_data['growth'][0]['5Y Net Income Growth (per Share)'])
            price = float(self.quote_data[0]['price'])
            csv_writer.writerow([ticker.rstrip(), price, eps, eps_growth])

#    def output_csv(self, ticker, csv_writer):
#        """Given the ticker and a csv_file (from csv package) - output a bunch fo data to a CSV"""
        # extract out the data we need
#        eps = float(self.financial_data['financials'][0]['EPS'])
#        eps_growth = float(self.growth_data['growth'][0]['5Y Net Income Growth (per Share)'])
#        price = float(self.quote_data[0]['price'])

#        csv_writer.writerow({'ticker': ticker, 'eps': eps, 'eps_growth': eps_growth})


#if __name__ == "__main__":
    
#    parser = argparse.ArgumentParser()
#    parser.add_argument("ticker", help="Stock ticker symbol", nargs="*", default=["AAPL"])
#    args = parser.parse_args()

#    csv_file = open("output.csv", mode='w')
#    fieldnames = ['ticker', 'eps', 'eps_growth']
#    writer = csv.DictWriter(csv_file, fieldnames=fieldnames,delimiter=',')
#    writer.writeheader()

fmp = FinanceModelingPrep()
   
#    tickers = args.ticker
with open("Stock Data Output.csv", mode = "w") as Output:
    header = ['Ticker', 'Price', 'EPS', 'EPS Growth (5 Yr)']                    
    csv_writer = csv.writer(Output, delimiter = ',')
    csv_writer.writerow(header)

#   """Opens the list of stock tickers that we are getting data for"""
with open("Stocks.txt", "r") as file:
    lines = []
    for ticker in file:
        fmp.get_stock_data(ticker.rstrip())
        valuation = fmp.get_valuation(ticker)
        fmp.write_to_csv(ticker)        


#    print("{:<16s} {:<16s} {:<16s} {:<16s} {:<16s}".format("Ticker", "Price", "Value Exp", "Value Gr.", "P/V Ratio"))
    
#    for ticker in tickers:
#        fmp.get_stock_data(ticker)
#        valuation = fmp.get_valuation(ticker)
#        fmp.output_csv(ticker, writer)

#    csv_file.close()
