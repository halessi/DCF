# DCF: Discounted Cash Flows

I've worked to create this as part of an effort to familiarize myself with calculating intrinsic value and discounted cash flows. 

I have found tweaking each of the configurable variables (CapEx growth, Revenue growth, discount rate, etc) to help with developing an insight into how the assumptions made when doing discounted cash flows play a role on the end valuation. This insight is essential to utilizing DCF effectively.

This library also enables comparisons to where the underlying entity has traded over the historical DCFs calculated, enabling an immediate visual comparison of where the stock has traded in relation to its intrinsic value.

**Obviously one cannot utilize this visualization to say very much about the quality of the DCF and assumptions made.** It is much more helpful when one is very __certain of the valuation they've derived__ and is hoping to understand how the stock has traded in relation to that in the past, i.e. at a premium or discount.

Next steps: implement dynamic discount rate calculation, multivariable earnings growth rate calculations, EBITDA multiples for terminal value

### Dependencies

```pip install matplotlib urllib seaborn```

### Basic usage

As of now, command line arguments are used to parse parameters. See main.py for defaults. Here is a description of the parameters: (as of now)

```python main.py \
        --period        # how many years to directly forecast Free Cash Flows to Firm
        --ticker        # ticker of the company, used for pulling financials
        --years         # if computing historical DCFs, the number of years back to compute
        --interval      # can compute DCFs historically on either an 'annual' or 'quarter' basis. if quarter is indicated, total number of DCFS = years * 4
        --step_increase # sensitivity analysis: if this is specified, DCFs will be computed for default + (step_increase * interval_number), showing specifically how changing the underlying assumption impacts valuation
        --steps         # number of steps to take (for step_increase)
        --variable      # the variable to increase each step, those available are: earnings_growth_rate, cap_ex_growth_rate, perpetual_growth_rate, discount_rate, [more to come..]
        --discount_rate # specified discount_rate (W.A.C.C., it'd be nice (i think) if we dynamically calculated this)
        --earnings_growth_rate # specified rate of earnings growth (EBIT)
        --perpetual_growth_rate # specified rate of perpetual growth for calculating terminal value after __period__ years, EBITDA multiples coming
```


### Examining the impact of changing the discount rate on Net Present Value

[something here]
