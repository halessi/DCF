import argparse

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



def main(args):
    '''
    a basic 2-stage DCF valuation model (i think)
    '''
    fcff = ulFCF(ebit, tax_rate, non_cash_charges, cwc, cap_ex)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '-period', help = 'years to forecast', type = int)
    parser.add_argument()

    args = parser.parse_args()
    main(args)