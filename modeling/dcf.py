import argparse
from decimal import Decimal

from modeling.data import *

def DCF(ticker, forecast, earnings_growth_rate, cap_ex_growth_rate, perpetual_growth_rate, year = 0):
    '''
    a very basic 2-stage DCF implemented for learning purposes.
    see enterprise_value() for details on arguments. 

    args:
        year: if 0, returns the most recent DCF valuation available. works in years-back, e.g. year = 1 would give (most recent - 1) DCF

    returns:
        dict: {'share price': __, 'enterprise_value': __, 'equity_value': __, 'date': __}
        CURRENT DCF VALUATION. See historical_dcf to fetch a history. 

    '''
    if ticker is not None:
        income_statement = get_income_statement(ticker = ticker)['financials'][year:year+2] # pass year + 1 bc we need change in working capital
        balance_statement = get_balance_statement(ticker = ticker)['financials'][year:year+2]
        cashflow_statement = get_cashflow_statement(ticker = ticker)['financials'][year:year+2]

        enterprise_val = enterprise_value(income_statement,
                                          cashflow_statement,
                                          balance_statement,
                                          forecast, 
                                          earnings_growth_rate, 
                                          cap_ex_growth_rate, 
                                          perpetual_growth_rate)
    else:
        raise ValueError('Must specify a ticker.') 

    enterprise_value_statement = get_EV_statement(ticker)['enterpriseValues'][0]
    equity_val, share_price = equity_value(enterprise_val,
                                       enterprise_value_statement)

    print('\nEnterprise Value for {}: ${}.'.format(ticker, '%.2E' % Decimal(str(enterprise_val))), 
              '\nEquity Value for {}: ${}.'.format(ticker, '%.2E' % Decimal(str(equity_val))),
           '\nPer share value for {}: ${}.\n'.format(ticker, '%.2E' % Decimal(str(share_price))),
            '-'*60)

    return {
        'date': income_statement[0]['date'],       # statement date used
        'enterprise_value': enterprise_val,
        'equity_value': equity_val,
        'share_price': share_price
    }

def historical_DCF(ticker, years, forecast, earnings_growth_rate, cap_ex_growth_rate, perpetual_growth_rate):
    '''
    Wrap DCF to fetch DCF values over a historical timeframe, denoted period. 

    args:
        same as DCF, except for
        period: number of years to fetch DCF for

    returns:
        {'date': dcf, ..., 'date', dcf}
    '''
    dcfs = {}
    for year in range(0, years):
        try:
            dcf = DCF(ticker, forecast, earnings_growth_rate,  cap_ex_growth_rate, perpetual_growth_rate, year = year)
        except IndexError:
            print('Year {} unavailable, no historical statement.'.format(year)) # catch
        dcfs[dcf['date'][0:4]] = dcf 
    
    return dcfs

def ulFCF(ebit, tax_rate, non_cash_charges, cwc, cap_ex):
    '''
    Formula to derive unlevered free cash flow to firm. Used in forecasting.

    args:
        ebit: Earnings before interest payments and taxes.
        tax_rate: The tax rate a firm is expected to pay. Usually a company's historical effective rate.
        non_cash_charges: Depreciation and amortization costs. 
        cwc: Annual change in net working capital.
        cap_ex: capital expenditures, or what is spent to maintain zgrowth rate.

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

def equity_value(enterprise_value, enterprise_value_statement):
    '''
    Given an enterprise value, return the equity value by adjusting for cash/cash equivs. and total debt.

    args:
        enterprise_value: (EV = market cap + total debt - cash), or total value
        enterprise_value_statement: information on debt & cash
    
    returns:
        equity_value: (enterprise value - debt + cash)
        share_price: equity value/shares outstanding
    '''
    equity_val = enterprise_value - enterprise_value_statement['+ Total Debt'] 
    equity_val += enterprise_value_statement['- Cash & Cash Equivalents']
    share_price = equity_val/float(enterprise_value_statement['Number of Shares'])

    return equity_val,  share_price

def enterprise_value(income_statement, cashflow_statement, balance_statement, period, earnings_growth_rate, cap_ex_growth_rate, perpetual_growth_rate):
    '''
    Calculate enterprise value by NPV of explicit _period_ free cash flows + NPV of terminal value,
    both discounted by W.A.C.C.

    args:
        ticker: company for forecasting
        period: years into the future
        earnings growth rate: assumed growth rate in earnings, YoY
        cap_ex_growth_rate: assumed growth rate in cap_ex, YoY
        perpetual_growth_rate: assumed growth rate in perpetuity for terminal value, YoY

    returns:
        enterprise value
    '''
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

    # Now let's iterate through years to calculate FCF, starting with most recent year
    print('Forecasting flows for {} years out, starting with at date {}.'.format(period, income_statement[0]['date']),
         ('\n         DFCF   |    EBIT   |    D&A    |    CWC     |   CAP_EX   | '))
    for yr in range(1, period+1):    

        # increment each value by growth rate
        ebit = ebit * (1 + earnings_growth_rate)
        non_cash_charges = non_cash_charges * (1 + earnings_growth_rate)
        cwc = cwc * 0.9                             # TODO: evaluate this cwc rate? 0.1 annually?
        cap_ex = cap_ex * (1 + cap_ex_growth_rate)         

        # discount by WACC
        flow = ulFCF(ebit, tax_rate, non_cash_charges, cwc, cap_ex)
        PV_flow = flow/(1 + discount)**yr
        flows.append(PV_flow)

        print(str(int(income_statement[0]['date'][0:4]) + yr) + '  ',
              '%.2E' % Decimal(PV_flow) + ' | ',
              '%.2E' % Decimal(ebit) + ' | ',
              '%.2E' % Decimal(non_cash_charges) + ' | ',
              '%.2E' % Decimal(cwc) + ' | ',
              '%.2E' % Decimal(cap_ex) + ' | ')

    NPV_FCF = sum(flows)
    
    # now calculate terminal value
    final_cashflow = flows[-1] * (1 + perpetual_growth_rate)
    TV = final_cashflow/(discount - perpetual_growth_rate)
    NPV_TV = TV/(1+discount)**(1+period)

    return NPV_TV+NPV_FCF

if __name__ == '__main__':
    '''run directly to fetch DCF of a company'''
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--ticker', help = 'ticker of company', type = str)
    parser.add_argument('-p', '--period', help = 'years to forecast', type = int, default =  5)
    parser.add_argument('-eg', '--earnings_growth_rate', help = 'growth in revenue, YoY',  type = float, default = .05)
    parser.add_argument('-cg', '--cap_ex_growth_rate', help = 'growth in cap_ex, YoY', type = float, default = 0.045)
    parser.add_argument('-pgr', '--perpetual_growth_rate', help = 'for perpetuity growth terminal value', type = float, default = 0.05)

    args = parser.parse_args()
    dcf = DCF(args.ticker, args.period, args.earnings_growth_rate, args.cap_ex_growth_rate, args.perpetual_growth_rate)