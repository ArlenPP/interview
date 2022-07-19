#! /usr/bin/env python3

# standard imports
import abc
import datetime
# third-party imports
from pickle import dump
from pickle import load
import pandas as pd
import numpy as np
# local import
from data.gen_data import build_XY


class Trader(metaclass=abc.ABCMeta):
    def __init__(self, model, start, end, feature_days, select_features, strategy_id):
        self.model = model
        self.train_start = start
        self.train_end = end
        self.feature_days = feature_days
        self.select_features = select_features
        self.train_strategy = strategy_id

    def write_info(self, name, descrip):
        self.name = name
        self.descrip = descrip

    def show_info(self):
        print(f'Start_date: {self.start_date}')
        print(f'End_date: {self.end_date}')
        print(f'Feature_days: {self.feature_days}')

    def save(self, path):
        with open(path, 'wb') as f:
            dump(self, f)

    def train_is_earlier_than(self, start_date):
        try:
            datetime.datetime.strptime(start_date, '%Y/%m/%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY/MM/DD")
        
        if start_date > self.train_end: return True
        else: 
            raise ValueError(f'start_date: {start_date} is earlier than train end_date: {self.end_date}')
        
    @abc.abstractmethod
    def preprocess(self):
        return NotImplemented

    @abc.abstractmethod
    def predict(self):
        return NotImplemented


class MLBiMergeRegTrader(Trader):
    def preprocess(self, start_date, end_date):
        X, Y = build_XY(start_date, end_date, self.select_features, self.feature_days, self.train_strategy)
        X = X.drop(['Date'], axis=1)
        Y['rise'] = Y['result']['Call_result'].tolist()
        Y['fall'] = Y['result']['Put_result'].tolist()
        
        return np.array(X), Y
    
    def predict(self, start_date, end_date):
        self.train_is_earlier_than(start_date)
        X, Y = self.preprocess(start_date, end_date)
        rise_pred = self.model['rise_regressor'].predict(X)
        fall_pred = self.model['fall_regressor'].predict(X)
        action = []
        for r, f in zip(rise_pred, fall_pred):
            if r < 0 and f < 0:
                action.append(0)
            elif r >= f : action.append(1)
            else: action.append(-1)
        return action


class MLBiMergeTrader(Trader):
    def preprocess(self, start_date, end_date):
        X, Y = build_XY(start_date, end_date, self.select_features, self.feature_days, self.train_strategy)
        X = X.drop(['Date'], axis=1)
        Y['rise'] = [1 if 1 == y else 0 for y in Y['Y']]
        Y['fall'] = [1 if -1 == y else 0 for y in Y['Y']]
        return np.array(X), Y
    
    def predict(self, start_date, end_date):
        self.train_is_earlier_than(start_date)
        X, Y = self.preprocess(start_date, end_date)
        rise_pred = self.model['rise_classifier'].predict(X)
        fall_pred = self.model['fall_classifier'].predict(X)
        action = []
        for r, f in zip(rise_pred, fall_pred):
            if (0 == r == f) or (1 == r == f):
                action.append(0)
            elif 1 == r: action.append(1)
            elif 1 == f: action.append(-1)
        return action