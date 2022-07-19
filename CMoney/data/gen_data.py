#! /usr/bin/env python3

# standard imports
from datetime import date, timedelta, datetime
import os
from sys import modules, path
from bisect import bisect_left, bisect_right
path.append('./data')
# third-party imports
import pandas as pd
import numpy as np
import yfinance as yf
from pickle import dump, load
import talib
from talib import abstract
# local import
from feature_set import feature_set
import feature


stock = 'AAPL'
stock_data = []
strategy = {}
now = datetime.now().strftime("%H:%M")
today = date.today().strftime("%Y-%m-%d")
base_path = './data/temp/'


def date_to_index(dates, start, end): # {{{
    start_index = bisect_left(dates, start)
    end_index = bisect_right(dates, end)
    if end > dates[-1]: return start_index, end_index+1
    return start_index, end_index
    # }}}


def generate_feature(data, computed_features): # {{{
    # use talib to generate feature
    data = data.astype('float')
    # 改成 TA-Lib 可以辨識的欄位名稱
    data.rename(columns={"Open": "open", "High": "high", "Low":"low", "Close":"close", "Volume":"volume"} , inplace=True)
    ta_list = talib.get_functions()
    for tech_ind in ta_list:
        try:
            # tech_ind 為技術指標的代碼，透過迴圈填入，再透過 eval 計算出 output
            output = eval(f'abstract.{tech_ind}(data)')
            # 如果輸出是一維資料，幫這個指標取名為 tech_ind 本身；多維資料則不需要
            if pd.core.series.Series == type(output): output.name = tech_ind
            # 透過 merge 把輸出結果併入 df DataFrame
            data = pd.merge(data, pd.DataFrame(output), left_on = data.index, right_on = output.index)
            data = data.set_index('key_0')
        except Exception as e:
            print('-------------------')
            print(tech_ind)
            print(e)
            print('-------------------')

    # generate feature self define
    data['Date'] = data.index
    # 改 column name 以便self define 的 funciton 可以看懂
    data.rename(columns={"open": "Open", "high": "High", "low":"Low", "close":"Close", "volume":"Volume"} , inplace=True)
    data = data.to_dict('records')
    numerical = [v for v in data[0].keys() if v not in ['Date']]

    for v in data:
        v['Date'] = v['Date'].strftime("%Y/%m/%d")
        for f in numerical:
            if(v[f] == ''):
                continue
            v[f] = float(v[f])
    for f in computed_features:
        getattr(modules['feature'], f)(data, f)

    return data


def build_X(start_date, end_date, selected_features, feature_days):
    assert feature_days >= 0, f'feature days need to >= 0'
    
    start_date = datetime.strptime(start_date, '%Y/%m/%d').strftime('%Y/%m/%d')
    end_date = datetime.strptime(end_date, '%Y/%m/%d').strftime('%Y/%m/%d')
    dates = [v['Date'] for v in stock_data]
    start_index, end_index   = date_to_index(dates, start_date, end_date)
    
    rows = []
    for i in range(start_index, end_index):
        row = []
        if i >= len(dates): row.append(datetime.today().strftime('%Y/%m/%d'))
        else: row.append(stock_data[i]['Date'])
        
        if 0 == feature_days:
            row.extend([stock_data[i][v] for v in selected_features])
        else:
            for f in selected_features:
                row.extend([stock_data[j][f] for j in range(i-1, i-feature_days-1, -1)])
        rows.append(row)

    columns = ['Date']
    if 0 == feature_days:
        columns.extend([f'{f}_{0}' for f in selected_features])
    else:
        for f in selected_features:
            columns.extend([f'{f}_-{day}' for day in range(1, feature_days+1)])
    X = pd.DataFrame(data=rows, columns=columns)
    return X


def build_Y(start_date, end_date, strategy_id):
    _strategy = strategy[strategy_id][start_date : end_date]
    Y = []
    for i in range(len(_strategy)):
        y = 0
        if(_strategy['Call_take_profit'][i] == 1): y = 1
        elif(_strategy['Put_take_profit'][i] == 1): y = -1
        Y.append(y)
    Y_result = {
                    'Y': np.array(Y),
                    'result': _strategy[['Call_result', 'Put_result']]
                }
    return Y_result


def build_XY(start_date, end_date, selected_features, feature_days, strategy_id):
    X = build_X(start_date, end_date, selected_features, feature_days)
    Y = build_Y(start_date, end_date, strategy_id)
    return X, Y
    

def update_local_data():
    stock_pkl = {
        'strategy': {},
    }
    stk = yf.Ticker(stock)
    data = stk.history(period = 'max')
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    # build strategy result
    for i in range(1, 4):
        _data = data.copy()
        _data['Call_result'] =  (data.Open.shift(-i) - data.Open)
        _data['Put_result'] =  -(_data['Call_result'])
        _data['Cost'] = data.Open
        _data['Call_take_profit'] = np.where(_data.Call_result > 0, 1, 0)
        _data['Put_take_profit'] = np.where(_data.Put_result > 0, 1, 0)
        _data['Date'] = _data.index
        _data = _data.drop(['Open', 'High', 'Low', 'Close', 'Volume'], axis=1)
        stock_pkl['strategy'][i] = _data   
    # generate features
    stock_pkl['stock'] = generate_feature(data, feature_set['all'])
    dump(stock_pkl, open(f'{base_path+today}-{now}.pkl', "wb"))
    return stock_pkl


def smart_update():
    global stock_data, strategy
    update = False
    file_list = os.listdir(base_path)
    # check update or not
    if(0 == len(file_list)): 
        update =  True
    else:
        stock_pickle_name = os.path.splitext(file_list[0])[0]
        _date, _time = stock_pickle_name[:10], stock_pickle_name[11:]
        # 美國股市在台灣時間早上5:00收盤，所以早上7:00更新local data
        if((today != _date) or (today == _date and _time < "7:05" and now > "7:05")):
            update = True
            os.remove(f'{base_path+stock_pickle_name}.pkl')
    # read pickle or update local data
    if update:
        stock_pkl = update_local_data()
    else:
        with open(f'{base_path+stock_pickle_name}.pkl', 'rb') as f: 
            stock_pkl = load(f)
    stock_data = stock_pkl['stock']
    strategy = stock_pkl['strategy']


smart_update()