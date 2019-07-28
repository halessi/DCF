'''
Quick visualization toolkit. I'd like to build this out to be decently powerful
in terms of enaabling quick interpretation of DCF related data.
'''

import matplotlib.pyplot as plt

def visualize(dcf_prices, current_share_prices, regress = True):
    '''
    2d plot comparing dcf-forecasted per share price with
    where a list of stocks is currently trading

    args:
        dcf_prices: dict of {'ticker': price, ...} for dcf-values
        current_share_prices: dict of {'ticker': price, ...} for (guess)
        regress: regress a line of best fit, because why not

    returns:
        nada
    '''
    print(dcf_prices)
    print(current_share_prices)