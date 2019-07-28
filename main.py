'''
author: Hugh Alessi
date: Saturday, July 27, 2019  8:25:00 PM
description: Use primitive underlying DCF modeling to compare intrinsic per share price
    to current share price. 

future goals: 
    -- Formalize sensitivity analysis. x
    -- More robust revenue forecasts in FCF. 
    -- EBITA multiples terminal value calculation.
    -- More to be added.
'''

from modeling import *

def main():
    '''XXX: for now let's hardcode an example'''

    # ~~~rough technology sector, TODO: need a more detailed screen
    companies = ['AAPL', 'GOOG', 'AMD', 'INTC', 'IBM', 'HPQ', 'HPE', 'DELL', 'NFLX']

    for company in companies:
        calculated_share_price = DCF(company, args.p, args.eg, args.eg, args.cg, args.pgr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--period', help = 'years to forecast', type = int, default =  5)
    parser.add_argument('-ts', '--tickers', help = 'list of company tickers', type = list, default = [])
    parser.add_argument('-eg', '--earnings_growth_rate', help = 'growth in revenue, YoY',  type = float, default = .05)
    parser.add_argument('-cg', '--cap_ex_growth_rate', help = 'growth in cap_ex, YoY', type = float, default = 0.045)
    parser.add_argument('-pgr', '--perpetual_growth_rate', help = 'for perpetuity growth terminal value', type = float, default = 0.05)

    args = parser.parse_args()
    main(args)


