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

    if args.s > 0:
        if args.v == 'eg' or 'earnings_growth_rate':
            cond, dcfs = run_setup(args, variable = 'eg')
        elif args.v == 'discount_rate' or 'discount':
            cond, dcfs = run_setup(args, variable = 'discount')
        else:
            raise ValueError('If step (-- s) is > 0, you must specify the variable via --v. What was passed is invalid.')
    else:
        cond, dcfs = {}, {'Ticker': [args.t]}
        dcfs[args.t] = historical_DCF(args.t, args.y, args.p, args.d, args.eg, args.cg, args.pg, args.i)

    prettyprint(dcfs, args.y)

    visualize_bulk_historicals(dcfs, condition = cond)

def run_setup(args, variable):
    dcfs, cond = {}, {args.v: []}
    
    for increment in range(1, 6): # default to 5 steps?
        var = vars(args)[variable] * (1 + (args.s * increment))
        step = '{}: {}'.format(args.v, str(var)[0:4])

        cond[args.v].append(step)
        vars(args)[variable] = var
        dcfs[step] = historical_DCF(args.t, args.y, args.p, args.d, args.eg, args.cg, args.pg, args.i)

    return cond, dcfs

def multiple_tickers():
    '''
    can be called from main to spawn dcf/historical dcfs for 
    a list of tickers TODO: fully fix
    '''

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
    return NotImplementedError

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--p', '--period', help = 'years to forecast', type = int, default =  5)
    parser.add_argument('--t', '--ticker', help = 'pass a single ticker to do historical DCF', type = str, default = 'AAPL')
    parser.add_argument('--y', '--years', help = 'number of years to forecast for. default 1.', type = int, default = 1)
    parser.add_argument('--i', '--interval', help = 'interval period for each calc, either "annual" or "quarter"', default = 'annual')
    parser.add_argument('--s', '--step_increase', help = 'specify step increase for EG, CG, PG to enable comparisons.', type = float, default = 0)
    parser.add_argument('--v', '--variable', help = 'if --step_increase is specified, must specifiy variable to increase from: [earnings_growth_rate, discount_rate]', default = None)
    parser.add_argument('--d', '--discount_rate', help = 'discount rate for future cash flow to firm', default = 0.1)
    parser.add_argument('--eg', '--earnings_growth_rate', help = 'growth in revenue, YoY',  type = float, default = .05)
    parser.add_argument('--cg', '--cap_ex_growth_rate', help = 'growth in cap_ex, YoY', type = float, default = 0.045)
    parser.add_argument('--pg', '--perpetual_growth_rate', help = 'for perpetuity growth terminal value', type = float, default = 0.05)

    args = parser.parse_args()
    main(args)
