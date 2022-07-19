# standard
from sys import path
path.append('./')
import calendar
# third-party imports
import pandas as pd
import numpy as np
from pickle import dump
from sklearn import linear_model
# local imports
from exp import *
from util import delay
from data.gen_data import build_Y
from data.feature_set import feature_set
from evaluate import trade_stock
from evaluate import evaluate


randint = [1238, 9716, 8355, 5894, 2472,  586, 9652, 6847, 5742,   46, 6905,
       8180,  367,  327, 4996, 4739, 3550,  663, 7685, 7582, 4746, 5821,
       5518, 9566, 9703, 3644, 1117,  566, 6207, 3823, 2985, 7991,  730,
       8869, 2093, 2706, 2648, 5708, 4438,  953, 6781, 4035, 4227, 4698,
        824, 6569, 8841, 2721, 1932, 1262, 8329,  172, 3199, 2831, 2990,
       7535, 4346, 9253, 4711, 2057, 9075, 6039, 1121, 1396,  388, 9069,
       1595, 1175, 2619, 7249, 5253, 7004, 1705, 1992, 5752, 7890, 5783,
       9141, 2793, 1666,  955, 3385, 5892, 2380, 4994, 7192, 8144, 3619,
       9798, 3742, 7966, 6503, 1689, 9845, 4636, 3538, 2405, 6621, 5846,
       6990, 430]
randint = [0]

if '__main__' == __name__:
    
    results = []
    train_year = 7
    for y in range(2020, 2021):
        for seed in randint:
            train_start = f'{y-train_year}/01/01'
            eval_start = f'{y}/01/01'
            trader = CatBoostReg_raise_fall(train_start, delay(train_start, {'years':train_year}), 2, 3, feature_set['talib'], seed)
            actions = trader.predict(f'{y}/01/01', f'{y}/03/31')
            result = trade_stock(f'{y}/01/01', f'{y}/03/31', actions, 2)
            print(evaluate(result))
            print(result.daily_return.cumsum()[-1])