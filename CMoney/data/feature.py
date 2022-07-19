#!/usr/bin/env python3
from dateutil.parser import parse
import numpy as np

def Close_SMA5(data, key):
    for v in data:
        v[key] = v['Close'] / v['SMA5'] - 1


def Close_SMA10(data, key):
    for v in data:
        v[key] = v['Close'] / v['SMA10'] - 1


def Close_SMA20(data, key):
    for v in data:
        v[key] = v['Close'] / v['SMA20'] - 1


def Close_SMA60(data, key):
    for v in data:
        v[key] = v['Close'] / v['SMA60'] - 1


def Close_SMA60_condition(data, key):
    data[0][key] = 0
    for i in range(1, len(data)):
        v = data[i]
        if (not (v['High'] > v['SMA60'] > v['Low'])):
            v[key] = 0
        elif (data[i-1]['Close'] > data[i-1]['SMA60']):
            v[key] = -1
        else:
            v[key] = 1


def d(data, key, n):  # accurate since the n-th day
    frag = True
    for i in range(0, len(data)):
        if('RSV9' not in data[i].keys() and frag):
            continue
        elif(frag):
            frag = False
            data[i][key] = data[i]['RSV9']
            continue
        data[i][key] = (1/3) * data[i]['K9'] + (2/3) * data[i-1][key]


def D9(data, key):  # accurate since the 9-th day
    d(data, key, 9)


def diff(data, key, minuend, subtrahend):
    for v in data:
        v[key] = v[minuend] - v[subtrahend]


def diff_last(data, key, target):
    data[0][key] = 0
    last = data[0][target]
    for i in range(1, len(data)):
        data[i][key] = data[i][target] - last
        last = data[i][target]


def Diff_Close(data, key):
    diff_last(data, key, 'Close')


def Diff_Close_SMA5(data, key):
    diff(data, key, 'Close', 'SMA5')


def Diff_Close_SMA10(data, key):
    diff(data, key, 'Close', 'SMA10')


def Diff_Close_SMA20(data, key):
    diff(data, key, 'Close', 'SMA20')


def Diff_Close_SMA60(data, key):
    diff(data, key, 'Close', 'SMA60')


def Diff_High(data, key):
    diff_last(data, key, 'High')


def Diff_High_SMA5(data, key):
    diff(data, key, 'High', 'SMA5')


def Diff_High_SMA10(data, key):
    diff(data, key, 'High', 'SMA10')


def Diff_High_SMA20(data, key):
    diff(data, key, 'High', 'SMA20')


def Diff_High_SMA60(data, key):
    diff(data, key, 'High', 'SMA60')


def Diff_Low(data, key):
    diff_last(data, key, 'Low')


def Diff_Low_SMA5(data, key):
    diff(data, key, 'Low', 'SMA5')


def Diff_Low_SMA10(data, key):
    diff(data, key, 'Low', 'SMA10')


def Diff_Low_SMA20(data, key):
    diff(data, key, 'Low', 'SMA20')


def Diff_Low_SMA60(data, key):
    diff(data, key, 'Low', 'SMA60')


def Diff_Open(data, key):
    diff_last(data, key, 'Open')


def Diff_Open_Last_Close(data, key):
    data[0][key] = 0
    last = data[0]['Close']
    for i in range(1, len(data)):
        data[i][key] = data[i]['Open'] - last
        last = data[i]['Close']

def Diff_Open_Close(data, key):
    diff(data, key, 'Open', 'Close')


def Diff_Open_SMA5(data, key):
    diff(data, key, 'Open', 'SMA5')


def Diff_Open_SMA10(data, key):
    diff(data, key, 'Open', 'SMA10')


def Diff_Open_SMA20(data, key):
    diff(data, key, 'Open', 'SMA20')


def Diff_Open_SMA60(data, key):
    diff(data, key, 'Open', 'SMA60')


def Diff_Volume_MA5(data, key):
    for v in data:
        if 'MA5' not in v.keys():
            continue
        v[key] = (v['Volume'] - v['MA5']) / v['MA5']


def Diff_Volume_MA10(data, key):
    for v in data:
        if 'MA10' not in v.keys():
            continue
        v[key] = (v['Volume'] - v['MA10']) / v['MA10']

def High_SMA5(data, key):
    for v in data:
        v[key] = v['High'] / v['SMA5'] - 1


def High_SMA10(data, key):
    for v in data:
        v[key] = v['High'] / v['SMA10'] - 1


def High_SMA20(data, key):
    for v in data:
        v[key] = v['High'] / v['SMA20'] - 1


def High_SMA60(data, key):
    for v in data:
        v[key] = v['High'] / v['SMA60'] - 1


def k(data, key, n):  # accurate since the n-th day
    frag = True
    for i in range(0, len(data)):
        if('RSV9' not in data[i].keys() and frag):
            continue
        elif(frag):
            frag = False
            data[i][key] = data[i]['RSV9']
            continue
        data[i][key] = (1/3) * data[i]['RSV9'] + (2/3) * data[i-1][key]


def K9(data, key):  # accurate since the 9-th day
    k(data, key, 9)


def K_D_condition(data, key):
    # last = 1 if data[0]['K9'] > data[0]['D9'] else -1
    # data[0][key] = 0
    last = 1
    for i in range(1, len(data)):
        if 'K9' not in data[i].keys():
            continue
        v = data[i]
        this = 1 if v['K9'] > v['D9'] else -1
        v[key] = 0 if this == last else last
        last = this


def Low_SMA5(data, key):
    for v in data:
        v[key] = v['Low'] / v['SMA5'] - 1


def Low_SMA10(data, key):
    for v in data:
        v[key] = v['Low'] / v['SMA10'] - 1


def Low_SMA20(data, key):
    for v in data:
        v[key] = v['Low'] / v['SMA20'] - 1


def Low_SMA60(data, key):
    for v in data:
        v[key] = v['Low'] / v['SMA60'] - 1


def MA5(data, key):
    sma(data, key, 5, field='Volume')

def MA6(data, key):
    sma(data, key, 6, field='Volume')

def MA10(data, key):
    sma(data, key, 10, field='Volume')

def MA12(data, key):
    sma(data, key, 12, field='Volume')


def Open_SMA5(data, key):
    for v in data:
        v[key] = v['Open'] / v['SMA5'] - 1


def Open_SMA10(data, key):
    for v in data:
        v[key] = v['Open'] / v['SMA10'] - 1


def Open_SMA20(data, key):
    for v in data:
        v[key] = v['Open'] / v['SMA20'] - 1


def Open_SMA60(data, key):
    for v in data:
        v[key] = v['Open'] / v['SMA60'] - 1


def RSI(data, key, n):
    for i in range(n, len(data)):
        up = []
        down = []
        for x in range(n):
            if(data[i-x]['Close'] > data[i-x-1]['Close']):
                up.append(data[i-x]['Close'] - data[i-x-1]['Close'])
            else:
                down.append(data[i-x-1]['Close'] - data[i-x]['Close'])
        up_mean = np.array(up).sum()/n
        down_mean = np.array(down).sum()/n
        if 0 == up_mean+down_mean:
            data[i][key] = (up_mean / 0.00001)
        else:
            data[i][key] = (up_mean/(up_mean+down_mean))


def RSI6(data, key):
    RSI(data, key, 6)


def RSI12(data, key):
    RSI(data, key, 12)


def RSI6_RSI12_condition(data, key):
    for v in data:
        if 'RSI12' not in v.keys():
            continue
        elif (v['RSI6'] >= 0.79 and v['RSI12'] >= 0.79):
            v[key] = -1
        elif(0.2 > v['RSI6'] and 0.2 > v['RSI12']):
            v[key] = 1
        else:
            v[key] = 0


def RSI_condition(data, key):
    # last = 1 if data[0]['RSI6'] > data[0]['RSI12'] else -1
    # data[0][key] = 0
    last = 1
    for i in range(1, len(data)):
        if 'RSI12' not in data[i].keys():
            continue
        v = data[i]
        this = 1 if v['RSI6'] > v['RSI12'] else -1
        v[key] = 0 if this == last else this  # ! different to K_D_condition
        last = this


def rsv(data, key, n):  # accurate since the n-th day
    highs = [v['High'] for v in data]
    lows = [v['Low'] for v in data]
    for i in range(1, n):
        high = max([v for v in highs[:i]])
        low = min([v for v in lows[:i]])
        data[i][key] = (data[i]['Close'] - low) / (high - low + 0.00001)
    for i in range(n, len(data)):
        high = max([v for v in highs[i+1-n:i+1]])
        low = min([v for v in lows[i+1-n:i+1]])
        data[i][key] = (data[i]['Close'] - low) / (high - low + 0.00001)


def RSV9(data, key):  # accurate since the 9-th day
    rsv(data, key, 9)


def RSV9_condition(data, key):
    for v in data:
        if not ['RSV9']:
            continue
        if ('RSV9' not in v.keys()):
            continue
        if (1 >= v['RSV9'] >= 0.96):
            v[key] = -1
        elif (0.1 > v['RSV9']):
            v[key] = 1
        else:
            v[key] = 0


def sma(data, key, n, field='Close'):  # accurate since the n-th day
    sum = 0
    for i in range(n):
        sum += data[i][field]
        data[i][key] = sum / (i+1)
    for i in range(n, len(data)):
        sum += data[i][field] - data[i-n][field]
        data[i][key] = sum / n


def SMA5(data, key):  # accurate since the 5-th day
    sma(data, key, 5)


def SMA10(data, key):  # accurate since the 10-th day
    sma(data, key, 10)


def SMA20(data, key):  # accurate since the 20-th day
    sma(data, key, 20)


def SMA60(data, key):  # accurate since the 60-th day
    sma(data, key, 60)


def SMA5_SMA20_condition(data, key):
    last = 1 if data[0]['SMA5'] > data[0]['SMA20'] else -1
    data[0][key] = 0
    for i in range(1, len(data)):
        v = data[i]
        this = 1 if v['SMA5'] > v['SMA20'] else -1
        v[key] = 0 if this == last else last
        last = this