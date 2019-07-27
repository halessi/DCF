import argparse

from utils import *

def ulFCF(ebit, tax_rate, non_cash_charges, cwc, cap_ex):
    '''
    Formula to derive unlevered free cash flow to firm. Used in forecasting.

    args:
        ebit: Earnings before interest payments and taxes.
        tax_rate: The tax rate a firm is expected to pay. Usually a company's historical effective rate.
        non_cash_charges: Depreciation and amortization costs. 
        cwc: Annual change in working capital.
        cap_ex: capital expenditures, or what must be spent to maintain growth rate.

    returns:
        unlevered free cash flow
    '''
    return ebit * (1-tax_rate) + non_cash_charges + cwc - cap_ex

def forecast_flows(ticker, period, growth_rate):
    cashflow_statement 


def main(args):
    '''
    a basic 2-stage DCF valuation model (i think)
    '''
    if args.ticker is not None:
        sum_of_present_values = forecast_flows(args.ticker, args.period, args.growth_rate)
    else:
        raise ValueError('Must specify a ticker.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--period', help = 'years to forecast', type = int, default =  5)
    parser.add_argument('-t', '--ticker', help = 'ticker of company', type = str)
    parser.add_argument('-g', '--growth_rate', help = 'growth in revenue, YoY',  type = float, default = .05)

    args = parser.parse_args()
    main(args)