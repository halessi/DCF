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
    # TODO: implement
    return NotImplementedError

def visualize_historicals(dcfs, historical_share_prices):
    '''
    2d plot comparing dcf history to share price history
    '''
    dcf_share_prices = {}
    for k, v in dcfs.items():
        dcf_share_prices[dcfs[k]['date']] = dcfs[k]['share_price']

    x = list(dcf_share_prices.keys())
    y = [list(dcf_share_prices.values()),  list(historical_share_prices.values())]
    
    print(x, y)

    for xe, ye in zip(x, y):
        plt.scatter([xe] * len(ye), ye)
    
    plt.show()
