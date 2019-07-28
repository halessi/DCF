'''
author: Hugh Alessi
date: Saturday, July 27, 2019  8:25:00 PM
description: Use primitive underlying DCF modeling to compare intrinsic per share price
    to current share price. 

future goals: 
    -- Formalize sensitivity analysis. 
    -- More robust revenue forecasts in FCF. 
    -- EBITA multiples terminal value calculation.
    -- More to be added.
'''


import argparse

from modeling.data import *
from modeling.dcf import *
from visualization.plot import *
from visualization.printouts import *


def main(args):
    '''
    although the if statements are less than desirable, it allows rapid exploration of 
    historical or present DCF values for either a single or list of tickers.
    '''

    dcfs = {}
    # if args.ts is not None:
    #     '''list to forecast'''
    #     if args.y > 1:
    #         for ticker in args.ts:
    #             dcfs[ticker] =  historical_DCF(args.t, args.y, args.p, args.eg, args.cg, args.pgr)
    #     else:
    #         for ticker in args.tss:
    #             dcfs[ticker] = DCF(args.t, args.p, args.eg, args.cg, args.pgr)
    # elif args.t is not None:
    #     ''' single ticker'''
    #     if args.y > 1:
    #         dcfs[args.t] = historical_DCF(args.t, args.y, args.p, args.eg, args.cg, args.pgr)
    #     else:
    #         dcfs[args.t] = DCF(args.t, args.p, args.eg, args.cg, args.pgr)
    # else:
    #     raise ValueError('A ticker or list of tickers must be specified with --ticker or --tickers')

    earnings_growth_rates = [0.01, 0.05, 0.1, 0.15, 0.20, 0.25]
    for egr in earnings_growth_rates:
        dcfs[str(egr)] = historical_DCF(args.t, args.y, args.p, egr, args.cg, args.pgr)

    prettyprint(dcfs, args.y)

    visualize_bulk_historicals(dcfs, condition = {'earnings_growth_rates': earnings_growth_rates})

    # if args.t is not None:
    #     '''plot a single ticker's historicals'''
    #     #visualize_historicals(dcfs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--p', '--period', help = 'years to forecast', type = int, default =  5)
    parser.add_argument('--t', '--ticker', help = 'pass a single ticker to do historical DCF', type = str, default = 'AAPL')
    parser.add_argument('--y', '--years', help = 'number of years to forecast for. default 1.', type = int, default = 1)
    parser.add_argument('--ts', '--tickers', help = 'list of company tickers', type = list, default = None)
    parser.add_argument('--eg', '--earnings_growth_rate', help = 'growth in revenue, YoY',  type = float, default = .05)
    parser.add_argument('--cg', '--cap_ex_growth_rate', help = 'growth in cap_ex, YoY', type = float, default = 0.045)
    parser.add_argument('--pgr', '--perpetual_growth_rate', help = 'for perpetuity growth terminal value', type = float, default = 0.05)

    args = parser.parse_args()
    main(args)
