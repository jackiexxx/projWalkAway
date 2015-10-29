#cointegrating_check.py

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import pandas.io.data as web
from pandas.stats.api import ols
import pprint
import statsmodels.tsa.stattools as ts
import datetime



#sets up time series plot
def plot_price_ts(df, ts1, ts2):
    months = mdates.MonthLocator()  # every month
    fig, ax = plt.subplots()
    ax.plot(df.index, df[ts1], label=ts1)
    ax.plot(df.index, df[ts2], label=ts2)
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(datetime.datetime(2013, 1, 1), datetime.datetime(2015, 1, 1))
    ax.grid(True)
    fig.autofmt_xdate()

    plt.xlabel('Month/Year')
    plt.ylabel('Price ($)')
    plt.title('%s and %s Daily Prices' % (ts1, ts2))
    plt.legend()
    plt.show()

#sets up scatter plot
def plot_scatter_ts(df, ts1, ts2):
    plt.xlabel('%s Price ($)' % ts1)
    plt.ylabel('%s Price ($)' % ts2)
    plt.title('%s and %s Price Scatterplot' % (ts1, ts2))
    plt.scatter(df[ts1], df[ts2])
    plt.show()

#sets up residuals plot
def plot_resids(df):
    months = mdates.MonthLocator()  # every month
    fig, ax = plt.subplots()
    ax.plot(df.index, df["res"], label="Residuals")
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(datetime.datetime(2013, 1, 1), datetime.datetime(2015, 1, 1))
    ax.grid(True)
    fig.autofmt_xdate()

    plt.xlabel('Month/Year')
    plt.ylabel('Price ($)')
    plt.title('Residual Plot')
    plt.legend()

    plt.plot(df["res"])
    plt.show()

#fetch in data, note: "if" statement below should be removed
#if it is desired to use this in another program as a module. As it is currently written
#it ensures this will ONLY run stand alone.
if __name__ == "__main__":
    start = datetime.datetime(2013, 1, 1)
    end = datetime.datetime(2015, 1, 1)

    voo = web.DataReader("VOO", "yahoo", start, end)
    spy = web.DataReader("SPY", "yahoo", start, end)

    df = pd.DataFrame(index=voo.index)
    df["VOO"] = voo["Adj Close"]
    df["SPY"] = spy["Adj Close"]

    # plots time series
    plot_price_ts(df, "VOO", "SPY")

    # plots data scatter for vis inspection
    plot_scatter_ts(df, "VOO", "SPY")

    # ordinary least squares, determines beta
    res = ols(y=df['SPY'], x=df["VOO"])
    print res
    beta_hr = res.beta.x

    # determine residuals,aka error in fit at each point
    df["res"] = df["SPY"] - beta_hr*df["VOO"]

    # plot the residuals from ols
    plot_resids(df)

    # determine and pretty print the CADF test on residuals.
    # see "http://statsmodels.sourceforge.net/devel/index.html"
    # for statsmodels documentation.
    print ""
    print ""
    print ""
    cadf = ts.adfuller(df["res"])
    print "Cointegration Augmented Dicky Fuller results are:"
    print ""
    print ""
    print ""
    pprint.pprint(cadf)
