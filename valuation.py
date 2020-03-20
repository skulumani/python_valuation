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

    def output_csv(self, ticker, csv_writer):
        """Given the ticker and a csv_file (from csv package) - output a bunch fo data to a CSV"""
        # extract out the data we need
        eps = float(self.financial_data['financials'][0]['EPS'])
        eps_growth = float(self.growth_data['growth'][0]['5Y Net Income Growth (per Share)'])
        price = float(self.quote_data[0]['price'])

        csv_writer.writerow({'ticker': ticker, 'eps': eps, 'eps_growth': eps_growth})


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument("-t", "--ticker", help="Stock ticker symbol", nargs="*")
    group.add_argument("-a", "--all", help="Use stock_list.csv and get all data",
                        action="store_true")

    args = parser.parse_args()

    csv_file = open("output.csv", mode='w')
    fieldnames = ['ticker', 'eps', 'eps_growth']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames,delimiter=',')
    writer.writeheader()

    fmp = FinanceModelingPrep()
    
    print("{:<16s} {:<16s} {:<16s} {:<16s} {:<16s}".format("Ticker", "Price", "Value Exp", "Value Gr.", "P/V Ratio"))
    if args.ticker:
        tickers = args.ticker

        for ticker in tickers:
            fmp.get_stock_data(ticker)
            valuation = fmp.get_valuation(ticker)
            fmp.output_csv(ticker, writer)
    elif args.all:
        # read stocks from CSV and put in a big list
        with open("stock_list.csv") as input_file:
            tickers = input_file.readlines()
    
        tickers = [ticker.strip() for ticker in tickers]
        for ticker in tickers:
            # get data for each one
            try:
                fmp.get_stock_data(ticker)
                valuation = fmp.get_valuation(ticker)
                # write to CSV
                fmp.output_csv(ticker, writer)
            except: 
                print("{} has no data".format(ticker))

    csv_file.close()
