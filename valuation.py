# API to interface with https://financialmodelingprep.com/developer/docs/

from urllib.request import urlopen
from urllib.parse import urljoin
import json

class FinanceModelingPrep:
    
    url_base = "https://financialmodelingprep.com/api/v3/"

    def __init__(self):
        pass

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
        url = urljoin(self.url_base, "financials/income-statement/" + ticker)
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
        # return estimate value
        return (value_graham, price)

if __name__ == "__main__":
    ticker = "AAPL"

    fmp = FinanceModelingPrep()
    
    print(fmp.get_annual_financials(ticker)['financials'][0]['EPS'])
    print(fmp.get_growth(ticker)['growth'][0]['EPS Growth'])
    print(fmp.get_quote(ticker)[0]['price'])

    print(fmp.get_valuation(ticker))

