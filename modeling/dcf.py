import argparse
from decimal import Decimal

from statements import *

def DCF(ticker, period, earnings_growth_rate, cap_ex_growth_rate, perpetual_growth_rate):
    '''
    a very basic 2-stage DCF implemented for learning purposes.
    see enterprise_value() for details on arguments
    '''
    if args.ticker is not None:
        enterprise_val = enterprise_value(ticker,
                              period, 
                              earnings_growth_rate, 
                              cap_ex_growth_rate, 
                              perpetual_growth_rate)
    else:
        raise ValueError('Must specify a ticker.')

    # adjustments
    ev_statement = get_EV_statement(ticker)['enterpriseValues'][0]
    equity_val = enterprise_val - ev_statement['+ Total Debt'] 
    equity_val += ev_statement['- Cash & Cash Equivalents']
    share_price = equity_val/float(ev_statement['Number of Shares'])

    print('\nEnterprise Value for {}: ${}.'.format(args.ticker, '%.2E' % Decimal(str(enterprise_val))), 
          '\nEquity Value for {}: ${}.'.format(args.ticker, '%.2E' % Decimal(str(equity_val))),
          '\nPer share value for {}: ${}'.format(args.ticker, '%.2E' % Decimal(str(share_price))))

    return {
        'enterprise_value': enterprise_val,
        'equity_val': equity_val,
        'share_price': share_price
    }

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

def enterprise_value(ticker, period, earnings_growth_rate, cap_ex_growth_rate, perpetual_growth_rate):
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

    # Now let's iterate through years to calculate FCF, starting with most recent year
    print('\nForecasting flows for {} years out, starting with at date {} with earnings growth {}.'.format(period, income_statement[0]['date'], earnings_growth_rate))  
    print('         DFCF   |    EBIT   |    D&A    |    CWC     |   CAP_EX   | ')
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
    print('\nSum of future flows for {}: {}.'.format(ticker, '%.2E' % Decimal(str(NPV_FCF))))
    
    # now calculate terminal value
    final_cashflow = flows[-1] * (1 + perpetual_growth_rate)
    TV = final_cashflow/(discount - perpetual_growth_rate)
    NPV_TV = TV/(1+discount)**(1+period)
    print('\nTerminal value for {} in {} years: {}.'.format(ticker, 1+period, '%.2E' % Decimal(str(NPV_TV))))

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