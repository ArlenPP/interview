import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpl_finance as mpf
import scipy
from dateutil.relativedelta import relativedelta
from datetime import datetime


def plot_roi(df, plot=False, path=None):
    df['ROI'] = df['daily_return'].cumsum()
    df.drop(['daily_return', 'Date', 'PnL'], axis=1, inplace=True)
    if plot: fig = df.plot(rot=75)
    if path: fig.get_figure().savefig(path)
    return df


def plot_candlestick(ax, data):
    ax.set_xticks(range(0, len(data['Time']), 30))
    ax.set_xticklabels(data['Time'][::30], rotation=45)
    mpf.candlestick2_ochl(ax, data['Open'], data['Close'], data['High'], data['Low'],width=1, colorup='r', colordown='green',alpha=0.6)
    ax.grid()
    ax.set_ylabel('Price', size=20)


def plot_kbar(data, plot=True, path=None):
    fig = plt.figure(figsize=(13,10))
    ax = fig.add_subplot(1, 1, 1)
    plot_candlestick(ax, data)
    if(not plot): plt.close()
    if(path): 
        plt.savefig(path)
        plt.close()
    return fig


def formatPrice(n):
	return ("-$" if n < 0 else "$") + "{0:.2f}".format(abs(n))

def delay(date, feq):
    date = datetime.strptime(date, '%Y/%m/%d')
    date = date + relativedelta(**feq) - relativedelta(days=1)
    return datetime.strftime(date, '%Y/%m/%d')
