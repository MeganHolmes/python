"""Module providing operations pertaining to currencies"""
import requests
from bs4 import BeautifulSoup as bs
from dateutil.parser import parse
from pprint import pprint


def convert_usd_to_cad(usd):
    """
    Converts usd to cad

    Inputs: usd - how much usd to convert to cad

    Returns: cad - how much cad is equal to the usd input
    """

    return float(get_exchange_list_xrates()["Canadian Dollar"]*usd)

def get_exchange_list_xrates():
    """
    Get list of exchange rates
    From: https://thepythoncode.com/article/make-a-currency-converter-in-python

    Inputs: None

    Returns: list of exchange rates
    """
    # make the request to x-rates.com to get current exchange rates for common currencies
    content = requests.get(f"https://www.x-rates.com/table/?from=USD&amount=1").content
    # initialize beautifulsoup
    soup = bs(content, "html.parser")

    # get the exchange rates tables
    exchange_tables = soup.find_all("table")
    exchange_rates = {}
    for exchange_table in exchange_tables:
        for tr in exchange_table.find_all("tr"):
            # for each row in the table
            tds = tr.find_all("td")
            if tds:
                currency = tds[0].text
                # get the exchange rate
                exchange_rate = float(tds[1].text)
                exchange_rates[currency] = exchange_rate

    return exchange_rates