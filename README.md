
# Verifying Momentum Strategy

The goals of this project are:

1. Verify dual momentum by verifing both Absuolte momentum and in combination with relative.
2. Build set of reusable primitives

## Steup

### create a virtual environment

[WIP]

### Required Modules

Required modules are in *[requirements.txt](./requirements.txt)*.

To install all required module run the following command:

```bash
pip install -r requirements.txt
```

## Folder structure

- [data\tickers](./data/tickers) folder includes all the tickers downloaded
- [data\output](./data/output) includes saved results of verious runs. Format used is {tickername}_ABS_a{action}_lb{lookback size}.
  - Where ABS stands for the name of the algorithem, Absolute momentum,  *'a'* is the number of days between actions and *'lb'* is the size of the lookback window. So SPY_ABS_a5_lb253, means SPY absolute momentum with action evaluated (and taken) every 5 trading days and the lookback window size is 253 trading days
  - for example, [QQQ_ABS_a21_lb253](./data/output/QQQ_ABS_a21_lb253.csv)
- each algorithem result csv file includes the following coloumns: Date | Close | Daily return | lookback window | ABS Close | RISK.
  - *Date*:
  - *Close*: (do we need to use adjusted close?)
  - *Daily retun*: is precentage change from previous close;
  - *lookback window*: is percentage change between close[i] / close[i- lookback]
  - *ABS Close*: is the absolute momentum result
  - *RISK*: shows action points and the result of the momentum evaluation

## todo list

- [ ] should the algorithem use Adj Close or Close?
- [x] wrap absolute momentum algo in a method and in its own file
- [x] create a notebook for basic experiments
- [x] wrap all helper functions into module, that can be easily used from notebook and code
- [ ] add plot, to show spy vs. Abs + action points
- [ ] calc max DD; Alpha; Beta; Sharp; etc...
- [ ] run experiment on ABS Momentum across all permutation of action and lookback and compare results between different permutations
- [ ] consider using one file for all different permutation?
- [ ] add cash trigger (sma 200 S&P to exit, when do we return?)
- [ ] test all algorithms to start from the same date. That is from the max lookback window (so they all start from the same starting point.
- [ ] check the rate of change in the lookback window at crashes before/after... hypothesis for daily change rate or lookback is bigger before riskoff due to carsh
- [ ] consdier adding some sort of date/time to tickers folder of naming convention
- [ ] download list of all S&P tickers
- [ ] find top winners/ looser in S&P per action & window then compare returns
- [ ] run cash trigger on stocks (AAPL; MSFT; from the cash trigger book)

## reading material

- https://github.com/matt-dong/Absolute-Momentum
- pandas has a rank function (*yay*) df.rank(axis=1) --> axis=1 means on columns