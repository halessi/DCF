import argparse
from decimal import Decimal

from statements import *

def ulFCF(ebit, tax_rate, non_cash_charges, cwc, cap_ex):
    '''
    Formula to derive unlevered free cash flow to firm. Used in forecasting.

    args:
        ebit: Earnings before interest payments and taxes.
        tax_rate: The tax rate a firm is expected to pay. Usually a company's historical effective rate.
        non_cash_charges: Depreciation and amortization costs. 
        cwc: Annual change in net working capital.
        cap_ex: capital expenditures, or what is spent to maintain growth rate.

    returns:
        unlevered free cash flow
    '''
    return ebit * (1-tax_rate) + non_cash_charges + cwc + cap_ex

def get_discount_rate():
    '''
    Calculate the Weighted Average Cost of Capital (WACC) for our company.
    Used for consideration of existing capital structure.

    args:
    
    returns:
        W.A.C.C.
    '''
    return .1 # TODO: implement 

def forecast_flows(ticker, period, earnings_growth_rate, cap_ex_growth_rate):
    '''
    Forecast free cash flows _period_ years into future.

    args:
        ticker: company for forecasting
        period: years into the future
        growth rate: assumed growth rate in revenue, nwc, non-cash-charges YoY

    returns:
        sum of present values of flows, discounted by WACC
    '''
    income_statement = get_income_statement(ticker = ticker)['financials']
    balance_statement = get_balance_statement(ticker = ticker)['financials']
    cashflow_statement = get_cashflow_statement(ticker = ticker)['financials']

    # XXX: statements are returned as historical list, 0 most recent
    ebit = float(income_statement[0]['EBIT'])
    tax_rate = float(income_statement[0]['Income Tax Expense']) /  \
               float(income_statement[0]['Earnings before Tax'])
    non_cash_charges = float(cashflow_statement[0]['Depreciation & Amortization'])
    cwc = (float(balance_statement[0]['Total assets']) - float(balance_statement[0]['Total non-current assets'])) - \
          (float(balance_statement[1]['Total assets']) - float(balance_statement[1]['Total non-current assets']))
    cap_ex = float(cashflow_statement[0]['Capital Expenditure'])
    discount = get_discount_rate()

    flows = []

    # Now let's iterate through years, starting with most recent year
    print('\nForecasting flows for {} years out, starting with at date {} with earnings growth {}.'.format(period, income_statement[0]['date'], earnings_growth_rate))  
    print('         DFCF   |    EBIT   |    D&A    |    CWC    |   CAP_EX   | ')
    for yr in range(1, period+1):    

        # increment each value by growth rate
        ebit = ebit * (1 + earnings_growth_rate)
        non_cash_charges = non_cash_charges * (1 + earnings_growth_rate)
        cwc = cwc * 0.9                             # TODO: evaluate this cwc rate? 0.1 annually?
        cap_ex = cap_ex * (1 + cap_ex_growth_rate)         

        flow = ulFCF(ebit, tax_rate, non_cash_charges, cwc, cap_ex)
        discounted_flow = flow/(1 + discount)**yr
        flows.append(discounted_flow)

        print(str(int(income_statement[0]['date'][0:4]) + yr) + '  ',
              '%.2E' % Decimal(discounted_flow) + ' | ',
              '%.2E' % Decimal(ebit) + ' | ',
              '%.2E' % Decimal(non_cash_charges) + ' | ',
              '%.2E' % Decimal(cwc) + ' | ',
              '%.2E' % Decimal(cap_ex) + ' | ')

    return sum(flows) 


def main(args):
    '''
    a very basic 2-stage DCF implemented for learning purposes
    '''
    if args.ticker is not None:
        sum_of_present_values = forecast_flows(args.ticker, args.period, args.earnings_growth_rate, args.cap_ex_growth_rate)
    else:
        raise ValueError('Must specify a ticker.')

    print('\nSum of future flows for {}: {}.'.format(args.ticker, '%.2E' % Decimal(str(sum_of_present_values))))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--period', help = 'years to forecast', type = int, default =  5)
    parser.add_argument('-t', '--ticker', help = 'ticker of company', type = str)
    parser.add_argument('-eg', '--earnings_growth_rate', help = 'growth in revenue, YoY',  type = float, default = .05)
    parser.add_argument('-cg', '--cap_ex_growth_rate', help = 'growth in cap_ex, YoY', type = float, default = 0.045)

    args = parser.parse_args()
    main(args)