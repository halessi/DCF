# DCF: Discounted Cash Flow

If you notice any errors or have any questions/suggestions, please reach out! ***hughalessi@gmail.com*** 

I've worked to create this Python library as part of an effort to familiarize myself with calculating discounted cash flows  working directly with a company's financial statements.  :chart_with_upwards_trend: :chart_with_downwards_trend:

I have found tweaking each of the configurable variables (CapEx growth, Revenue growth, discount rate, etc) to help with developing an insight into how the assumptions made when doing discounted cash flows play a role on the end valuation. This insight is essential to utilizing DCF effectively.

This library also makes possible comparisons to where the underlying entity has traded over the historical DCFs calculated, enabling an immediate illustration of where the stock has traded in relation to its intrinsic value.

**Obviously one cannot utilize this visualization to say very much about the quality of their DCF and assumptions made.** It is much more helpful when one is very __certain of the valuation they've derived__ and is hoping to understand how the stock has traded in relation to that in the past, i.e., at a premium or discount.

Next steps: 
- [ ] implement dynamic discount rate calculation
- [ ] multivariable earnings growth rate calculations (as opposed to hard-coding)
- [ ] EBITDA multiples for terminal value

### Dependencies

```pip install matplotlib urllib3 seaborn```

### Basic usage

As of now, command line arguments are used to parse parameters. See main.py for default values. Here is a description of the parameters: (as of now)

```
python main.py \
        --period        
        --ticker        
        --years         
        --interval      
        --step_increase 
        --steps         
        --variable      
        --discount_rate 
        --earnings_growth_rate 
        --perpetual_growth_rate
        --apikey
```

  Argument              | Usage          
----------------------- | ------------------
period                  | how many years to directly forecast [Free Cash Flows](https://financeformulas.net/Free-Cash-Flow-to-Firm.html)
ticker                  | ticker of the company, used for pulling financials
years                   | if computing historical DCFs (i.e. years > 1), the number of years back to compute
interval                | can compute DCFs historically on either an 'annual' or 'quarter' basis. if quarter is indicated, total number of DCFS = years * 4
step_increase           | __some sensitivity analysis__: if this is specified, DCFs will be computed for default + (step_increase * interval_number), showing specifically how changing the underlying assumption impacts valuation
steps                   | number of steps to take (for step_increase)
variable                | the variable to increase each step, those available are: earnings_growth_rate, cap_ex_growth_rate, perpetual_growth_rate, discount_rate, [more to come..]
discount_rate           | specified discount_rate (W.A.C.C., it'd be nice (i think) if we dynamically calculated this)
earnings_growth_rate    | specified rate of earnings growth (EBIT)
perpetual_growth_rate   | specified rate of perpetual growth for calculating terminal value after __period__ years, EBITDA multiples coming
apikey                  | (Free) API Key to access financial data from [financialmodelingprep](https://financialmodelingprep.com/) -- Can also be provided as `APIKEY` envrionment variable.

### Example

If we want to examine historical DCFS for $AAPL, we can run:

```python main.py --t AAPL --i 'annual' --y 3 --eg .15 --steps 2 --s 0.1 --v eg --apikey <secret>```

or via:
```
export APIKEY=<secret>
python main.py --t AAPL --i 'annual' --y 3 --eg .15 --steps 2 --s 0.1 --v eg
```


This pulls the financials for AAPL for each year 3 years (--y) back to calculate 12 DCFs (3 years * 4 quarters), starting at a base earnings growth of 15% (--eg) and increasing for two steps (--steps) by 10% (--s), with --v specifying that earnings growth is the variable we want to increment. 

Terminal outputs some details just for us to keep an eye on:

```
Forecasting flows for 5 years out, starting at 2018-12-29. 
         DFCF   |    EBIT   |    D&A    |    CWC    |   CAP_EX   | 
2019   2.35E+10 |  2.79E+10 |  3.96E+09 |  2.17E+09 |  -3.51E+09 | 
2020   2.80E+10 |  3.70E+10 |  5.26E+09 |  1.52E+09 |  -3.82E+09 | 
2021   3.82E+10 |  5.54E+10 |  7.86E+09 |  1.06E+09 |  -4.34E+09 | 
2022   5.84E+10 |  9.19E+10 |  1.31E+10 |  7.44E+08 |  -5.12E+09 | 
2023   9.82E+10 |  1.68E+11 |  2.38E+10 |  5.21E+08 |  -6.27E+09 | 

Enterprise Value for AAPL: $1.41E+12. 
Equity Value for AAPL: $1.34E+12. 
Per share value for AAPL: $2.81E+02.
```
This provides a quick way to dive a bit deeper into what happened in the underlying calculations without necessarily needing to pull apart the code. 

![Optional Text](../master/imgs/AAPL_eg_long.png)

***Although far from a presentation-ready chart***, evident here is an increase in the DCF-forecasted per share value of AAPL that results from our specified increase in forecasted earnings growth (i.e. the variable we're examining). On the quarterly basis we see a large degree of seasonal variation, indicating that perhaps this particular DCF would benefit from a more specific [forecasting of cash flows](https://www.ersj.eu/repec/ers/papers/11_2_p2.pdf). 

### References

[1] http://people.stern.nyu.edu/adamodar/pdfiles/eqnotes/dcfcf.pdf                                                      
[2] http://people.stern.nyu.edu/adamodar/pdfiles/basics.pdf                                                     
[3] https://www.oreilly.com/library/view/valuation-techniques-discounted/9781118417607/xhtml/sec30.html                     
[4] https://www.cchwebsites.com/content/calculators/BusinessValuation.html
