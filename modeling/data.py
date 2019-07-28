'''
Utilizing financialmodelingprep.com for their free-endpoint API
to gather company financials.

NOTE: Some code taken directly from their documentation. See: https://financialmodelingprep.com/developer/docs/. 
'''

from urllib.request import urlopen
import json

def get_jsonparsed_data(url):
    '''
    Fetch url, return parsed json. 

    args:
        url: the url to fetch.
    
    returns:
        parsed json
    '''
    response = urlopen(url)
    data = response.read().decode('utf-8')
    return json.loads(data)

def get_EV_statement(ticker):
    '''
    Fetch EV statement, with details like total shares outstanding, from FMP.com

    args:
        ticker: company tickerr
    returns:
        parsed EV statement
    '''
    url = 'https://financialmodelingprep.com/api/v3/enterprise-value/{}'.format(ticker)
    return get_jsonparsed_data(url)

#! TODO: maybe combine these with argument flag for which statement, seems pretty redundant tbh
def get_income_statement(ticker, period = 'annual'):
    '''
    Fetch income statement.

    args:
        ticker: company ticker.
        period: annual default, can fetch quarterly if specified. 

    returns:
        parsed company's income statement
    '''
    if period == 'annual':
        url = 'https://financialmodelingprep.com/api/v3/financials/income-statement/{}'.format(ticker)
    elif period == 'quarter':
        url = 'https://financialmodelingprep.com/api/v3/financials/income-statement/{}?period=quarter'(ticker)
    else:
        raise ValueError("in get_income_statement: invalid period")     # may as well throw...

    return get_jsonparsed_data(url)


def get_cashflow_statement(ticker, period = 'annual'):
    '''
    Fetch cashflow statement.

    args:
        ticker: company ticker.
        period: annual default, can fetch quarterly if specified. 

    returns:
        parsed company's cashflow statement
    '''
    if period == 'annual':
        url = 'https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/{}'.format(ticker)
    elif period == 'quarter':
        url = 'https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/{}?period=quarter'(ticker)
    else:
        raise ValueError("in get_cashflow_statement: invalid period")     # may as well throw...

    return get_jsonparsed_data(url)

def get_balance_statement(ticker, period = 'annual'):
    '''
    Fetch balance sheet statement.

    args:
        ticker: company ticker.
        period: annual default, can fetch quarterly if specified. 

    returns:
        parsed company's balance sheet statement
    '''
    if period == 'annual':
        url = 'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{}'.format(ticker)
    elif period == 'quarter':
        url = 'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{}?period=quarter'(ticker)
    else:
        raise ValueError("in get_balancesheet_statement: invalid period")     # may as well throw...

    return get_jsonparsed_data(url)

def get_stock_price(ticker):
    '''
    Fetches the stock price for a ticker

    args:
        ticker
    
    returns:
        {'symbol': ticker, 'price': price}
    '''
    url = 'https://financialmodelingprep.com/api/v3/stock/real-time-price/{}'.format(ticker)
    return get_jsonparsed_data(url)

def get_batch_stock_prices(tickers):
    '''
    Fetch the stock prices for a list of tickers.

    args:
        tickers: a list of  tickers........
    
    returns:
        dict of {'ticker':  price}
    '''
    prices = {}
    for ticker in tickers:
        prices[ticker] = get_stock_price(ticker)['price']

    return prices

if __name__ == '__main__':
    ''' quick test, to use run data.py directly '''

    ticker = 'AAPL'
    data = get_cashflow_statement(ticker)
    print(data)
