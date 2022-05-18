"""
Utilizing financialmodelingprep.com for their free-endpoint API
to gather company financials.

NOTE: Some code taken directly from their documentation. See: https://financialmodelingprep.com/developer/docs/. 
"""

from urllib.request import urlopen
import json, traceback


def get_api_url(requested_data, ticker, period, apikey):
    if period == 'annual':
        url = 'https://financialmodelingprep.com/api/v3/{requested_data}/{ticker}?apikey={apikey}'.format(
            requested_data=requested_data, ticker=ticker, apikey=apikey)
    elif period == 'quarter':
        url = 'https://financialmodelingprep.com/api/v3/{requested_data}/{ticker}?period=quarter&apikey={apikey}'.format(
            requested_data=requested_data, ticker=ticker, apikey=apikey)
    else:
        raise ValueError("invalid period " + str(period))
    return url


def get_jsonparsed_data(url):
    """
    Fetch url, return parsed json. 

    args:
        url: the url to fetch.
    
    returns:
        parsed json
    """
    try: response = urlopen(url)
    except Exception as e:
        print(f"Error retrieving {url}:")
        try: print("\t%s"%e.read().decode())
        except: pass
        raise
    data = response.read().decode('utf-8')
    json_data = json.loads(data)
    if "Error Message" in json_data:
        raise ValueError("Error while requesting data from '{url}'. Error Message: '{err_msg}'.".format(
            url=url, err_msg=json_data["Error Message"]))
    return json_data


def get_EV_statement(ticker, period='annual', apikey=''):
    """
    Fetch EV statement, with details like total shares outstanding, from FMP.com

    args:
        ticker: company tickerr
    returns:
        parsed EV statement
    """
    url = get_api_url('enterprise-value', ticker=ticker, period=period, apikey=apikey)
    return get_jsonparsed_data(url)


#! TODO: maybe combine these with argument flag for which statement, seems pretty redundant tbh
def get_income_statement(ticker, period='annual', apikey=''):
    """
    Fetch income statement.

    args:
        ticker: company ticker.
        period: annual default, can fetch quarterly if specified. 

    returns:
        parsed company's income statement
    """
    url = get_api_url('financials/income-statement', ticker=ticker, period=period, apikey=apikey)
    return get_jsonparsed_data(url)


def get_cashflow_statement(ticker, period='annual', apikey=''):
    """
    Fetch cashflow statement.

    args:
        ticker: company ticker.
        period: annual default, can fetch quarterly if specified. 

    returns:
        parsed company's cashflow statement
    """
    url = get_api_url('financials/cash-flow-statement', ticker=ticker, period=period, apikey=apikey)
    return get_jsonparsed_data(url)


def get_balance_statement(ticker, period='annual', apikey=''):
    """
    Fetch balance sheet statement.

    args:
        ticker: company ticker.
        period: annual default, can fetch quarterly if specified. 

    returns:
        parsed company's balance sheet statement
    """
    url = get_api_url('financials/balance-sheet-statement', ticker=ticker, period=period, apikey=apikey)
    return get_jsonparsed_data(url)


def get_stock_price(ticker, apikey=''):
    """
    Fetches the stock price for a ticker

    args:
        ticker
    
    returns:
        {'symbol': ticker, 'price': price}
    """
    url = 'https://financialmodelingprep.com/api/v3/stock/real-time-price/{ticker}?apikey={apikey}'.format(
        ticker=ticker, apikey=apikey)
    return get_jsonparsed_data(url)


def get_batch_stock_prices(tickers, apikey=''):
    """
    Fetch the stock prices for a list of tickers.

    args:
        tickers: a list of  tickers........
    
    returns:
        dict of {'ticker':  price}
    """
    prices = {}
    for ticker in tickers:
        prices[ticker] = get_stock_price(ticker=ticker, apikey=apikey)['price']

    return prices


def get_historical_share_prices(ticker, dates, apikey=''):
    """
    Fetch the stock price for a ticker at the dates listed.

    args:
        ticker: a ticker.
        dates: a list of dates from which to fetch close price.

    returns:
        {'date': price, ...}
    """
    prices = {}
    for date in dates:
        try: date_start, date_end = date[0:8] + str(int(date[8:]) - 2), date
        except:
            print(f"Error parsing '{date}' to date.")
            print(traceback.format_exc())
            continue
        url = 'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?from={date_start}&to={date_end}&apikey={apikey}'.format(
            ticker=ticker, date_start=date_start, date_end=date_end, apikey=apikey)
        try:
            prices[date_end] = get_jsonparsed_data(url)['historical'][0]['close']
        except IndexError:
            #  RIP nested try catch, so many issues with dates just try a bunch and get within range of earnings release
            try:
                prices[date_start] = get_jsonparsed_data(url)['historical'][0]['close']
            except IndexError:
                print(date + ' ', get_jsonparsed_data(url))

    return prices


if __name__ == '__main__':
    """ quick test, to use run data.py directly """

    ticker = 'AAPL'
    apikey = '<DEMO>'
    data = get_cashflow_statement(ticker=ticker, apikey=apikey)
    print(data)
