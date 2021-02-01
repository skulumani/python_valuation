#!/usr/bin/env python3
# API to interface with https://financialmodelingprep.com/developer/docs/

from urllib.request import urlopen
from urllib.parse import urljoin
import json
import argparse
import csv


# Defining class that has functions to pull data from website
class FinanceModelingPrep:
    

    def __init__(self):
        self.url_base = "https://www.alphavantage.co/query?function="

    def get_data(self, url):
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)

    def get_profile(self, ticker):
        url = urljoin(self.url_base, "OVERVIEW&symbol=" +  ticker + api_key)
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
    
#   Is this used?
    def form_ticker_string(self, tickers):
        """Form a comma seperate list of tickers. Then can be appended to the URL"""
        ticker_string = ""
        for ticker in tickers:
            ticker_string = ticker_string + ticker + ","

        return ticker_string

    def get_stock_data(self, tickers):
        """Single function to get all the data and store as member variables"""
        self.profile_data = self.get_profile(ticker) 
        self.financial_data = self.get_annual_financials(ticker)
        self.growth_data = self.get_growth(ticker)
        self.quote_data = self.get_quote(ticker)
        self.key_metrics_data = self.get_key_metrics(ticker)
        self.financial_ratios_data = self.get_ratios(ticker)


    def get_valuation(self, ticker):
        # extract out the data we need
        eps = float(self.financial_data['financials'][0]['EPS'])
        eps_growth = float(self.growth_data['growth'][0]['5Y Net Income Growth (per Share)'])
        price = float(self.quote_data[0]['price'])
       
        # compute graham valuation and exponential growth valuation
        value_graham = eps * (8.5 + 2 * eps_growth*100)
        value_exp = eps * 12 * (1 + eps_growth)**5
        print("{:<16s} {:<2.2f} {:<16.2f} {:<16.2f} {:<16.2f}".format(ticker,
                                                                  price,
                                                                  value_exp, 
                                                                  value_graham, 
                                                                  price/value_exp))
        # return estimate value
        return (price, value_exp, value_graham)

#   """Writes stock data to CSV"""
    def write_to_csv(self, ticker):
        with open("Stock Data Output_test.csv", mode = "a", newline = '\n') as Output:
            csv_writer = csv.writer(Output, delimiter = ',')
            company_name = str(self.profile_data['Name'])
            industry = str(self.profile_data['Industry'])
            sector = str(self.profile_data['Sector'])
            #price = float(self.quote_data[0]['price'])            
            eps_annual = float(self.financial_data['annualEarnings'][0]['reportedEPS'])
            eps_
            eps_growth = float(self.growth_data['growth'][0]['5Y Net Income Growth (per Share)'])
            research_cost = float(self.financial_data['financials'][0]['R&D Expenses'])/1000000
            pe_ratio = float(self.key_metrics_data['metrics'][0]['PE ratio'])
            ps_ratio = float(self.key_metrics_data['metrics'][0]['Price to Sales Ratio'])
            pb_ratio = float(self.key_metrics_data['metrics'][0]['PB ratio'])
            pcf_ratio = float(self.key_metrics_data['metrics'][0]['POCF ratio'])
            pfcf_ratio = float(self.key_metrics_data['metrics'][0]['PFCF ratio'])
            op_margin = float(self.financial_ratios_data['ratios'][0]['profitabilityIndicatorRatios']['operatingProfitMargin'])
            net_margin = float(self.financial_ratios_data['ratios'][0]['profitabilityIndicatorRatios']['netProfitMargin'])
            debt_equity = float(self.key_metrics_data['metrics'][0]['Debt to Equity'])

            csv_writer.writerow([ticker.rstrip(), company_name, sector, industry, price, f"{eps: 6.2f}", f"{eps_growth: 6.2f}", f"{research_cost: 12.2f}", f"{pe_ratio: 6.2f}", f"{ps_ratio: 6.2f}", f"{pb_ratio: 6.2f}", f"{pcf_ratio: 6.2f}", f"{pfcf_ratio: 6.2f}", f"{op_margin: 0.2f}", f"{net_margin: 0.2f}", f"{debt_equity: 6.2f}"])


#   """Assigns 'fmp' as the variable for the class"""
fmp = FinanceModelingPrep()
   
#Current API Key
api_key = "4P4EU3M6PAK0XAYR"

#   """"Writes the header row to the csv file"""
with open("Stock Data Output_test.csv", mode = "w") as Output:
    header = ['Ticker', 'Company Name', 'Sector', 'Industry', 'Price', 'EPS', 'EPS Growth (5 Yr)', 'R&D Expenses ($M)', 'PE', 'PS', 'P/B', 'P/CF', 'P/FCF', 'Operating Margin', 'Net Margin', 'Debt to Equity']                    
    csv_writer = csv.writer(Output, delimiter = ',')
    csv_writer.writerow(header)


#   """Opens the list of stock tickers that we are getting data for"""
with open("stock_list.txt", "r") as file:
    lines = []
    for ticker in file:
        try:        
            fmp.get_stock_data(ticker.rstrip())
#            valuation = fmp.get_valuation(ticker.rstrip())
            fmp.write_to_csv(ticker.rstrip())
        except:
            pass
            print("Could not reach site for" + ticker)        

