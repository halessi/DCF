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


def get_income_statement(ticker, period = 'annual'):
    '''
    Fetch income statement.

    args:
        ticker: company ticker.
        period: annual default, can fetch quarterly if specified. 
s
    returns:
        parsed company's income statement
    '''
    if ticker == 'annual':
        url = 'https://financialmodelingprep.com/api/v3/financials/income-statement/{}'.format(ticker)
    else:
        url = 'https://financialmodelingprep.com/api/v3/financials/income-statement/{}?period=quarter'(ticker)
    return get_jsonparsed_data(url)


if __name__ == '__main__':
    ''' quick test, to use run data.py directly '''

    url = "https://financialmodelingprep.com/api/company/profile/AAPL?datatype=json"
    data = get_jsonparsed_data(url)
    print(data)
