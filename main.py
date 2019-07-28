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

import argparse
from modeling.dcf import *
from modeling.data import *
from visualization.plot import *

def main(args):
    if args.ticker is not None:
        # do historical DCF first
        dcf_over_time = historical_DCF(args.ticker, args.period, args.forecast, args.eg, args.cg, args.pgr)
        print(dcf_over_time)
        exit()

        share_price_over_time = historical_share_price(args.ticker, date_start, date_end)

    # # calculate DCF for each
    # for company in companies:
    #     calculated_share_price = DCF(args.ticker, args.p, args.eg, args.cg, args.pgr).get('share_price')
    #     dcf_share_prices[company] = calculated_share_price


        
    # plot
    visualize(dcf_share_prices, current_share_prices)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--p', '--period', help = 'years to forecast', type = int, default =  5)
    parser.add_argument('--t', '--ticker', help = 'pass a single ticker to do historical DCF', type = str)
    parser.add_argument('--ts', '--tickers', help = 'list of company tickers', type = list, default = [])
    parser.add_argument('--eg', '--earnings_growth_rate', help = 'growth in revenue, YoY',  type = float, default = .05)
    parser.add_argument('--cg', '--cap_ex_growth_rate', help = 'growth in cap_ex, YoY', type = float, default = 0.045)
    parser.add_argument('--pgr', '--perpetual_growth_rate', help = 'for perpetuity growth terminal value', type = float, default = 0.05)

    args = parser.parse_args()
    main(args)


