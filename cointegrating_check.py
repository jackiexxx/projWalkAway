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

#enter ticker symbols here
inst_x = "LMT"
inst_y = "RTN"

#enter info for start stop dates, year xxxx, month yy, day zz
#note if day or month is single digit, use single digit only, eg july = 7
start_year = 2013
end_year = 2014
start_month_num = 1
end_month_num = 7
start_day_num = 1
end_day_num = 15

#sets up time series plot
def plot_price_ts(df, ts1, ts2):
    months = mdates.MonthLocator()  # every month
    fig, ax = plt.subplots()
    ax.plot(df.index, df[ts1], label=ts1)
    ax.plot(df.index, df[ts2], label=ts2)
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(datetime.datetime(start_year, start_month_num, start_day_num), datetime.datetime(end_year, end_month_num, end_day_num))
    ax.grid(True)
    fig.autofmt_xdate()

    plt.xlabel('Month/Year')
    plt.ylabel('Price ($)')
    plt.title('%s and %s Daily Prices' % (ts1, ts2))
    plt.legend()
    plt.show()

#sets up spread plot
def plot_spread(df):
    months = mdates.MonthLocator()  # every month
    fig, ax = plt.subplots()
    ax.plot(df.index, df["SPREAD"], label="Daily Price Spread")
    ax.plot(df.index, df["MEAN SPREAD"], label="Mean Spread")
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(datetime.datetime(start_year, start_month_num, start_day_num), datetime.datetime(end_year, end_month_num, end_day_num))
    ax.grid(True)
    fig.autofmt_xdate()

    plt.xlabel('Month/Year')
    plt.ylabel('Price Spread ($)')
    plt.title('Price Spread')
    plt.legend()

    plt.plot(df["SPREAD"])
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
    ax.set_xlim(datetime.datetime(start_year, start_month_num, start_day_num), datetime.datetime(end_year, end_month_num, end_day_num))
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
    start = datetime.datetime(start_year, start_month_num, start_day_num)
    end = datetime.datetime(end_year, end_month_num, end_day_num)

    x_term = web.DataReader(inst_y, "yahoo", start, end)
    y_term = web.DataReader(inst_x, "yahoo", start, end)

    df = pd.DataFrame(index=x_term.index)
    df[inst_y] = x_term["Adj Close"]
    df[inst_x] = y_term["Adj Close"]
    df["SPREAD"] = x_term["Adj Close"]-y_term["Adj Close"]
    df["MEAN SPREAD"] = df["SPREAD"].mean()

    # plots time series
    plot_price_ts(df, inst_y, inst_x)

    # plots price spread
    plot_spread(df)

    # plots data scatter for vis inspection
    plot_scatter_ts(df, inst_y, inst_x)

    # ordinary least squares, determines beta
    res = ols(y=df[inst_x], x=df[inst_y])
    beta_hr = res.beta.x

    # determine residuals,aka error in fit at each point
    df["res"] = df[inst_x] - beta_hr*df[inst_y]

    # plot the residuals from ols
    plot_resids(df)

    # determine and pretty print the CADF test on residuals.
    # see "http://statsmodels.sourceforge.net/devel/index.html"
    # for statsmodels documentation.
    print "#############################"
    print "#############################"
    print "#############################"
    print res
    print ""
    print ""
    print "#############################"
    print "#############################"
    print "#############################"
    print ""
    print ""
    print "Hedge Ratio is" + str(beta_hr)
    print ""
    print ""
    print "#############################"
    print "#############################"
    print "#############################"
    print ""
    print ""
    cadf = ts.adfuller(df["res"])
    print "Cointegration Augmented Dicky Fuller results are:"
    print ""
    pprint.pprint(cadf)
