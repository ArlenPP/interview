from sys import path
path.append('./')
from data.gen_data import build_XY
from model.Trader import *
from sklearn.model_selection import train_test_split
from inspect import signature
import random
import numpy as np
from xgboost import XGBClassifier
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import lightgbm as lgb


def build_clf(clf, x, y, cv=None, **kwargs):
    keys = set(kwargs.keys()) & set(signature(clf.__init__).parameters)
    args = { key: kwargs[key] for key in keys }

    # if 'early_stopping_rounds' in kwargs:
    #     X1, X2, y1, y2 = train_test_split(x, y, random_state=kwargs['random_state'], test_size=kwargs['test_size'])
    #     clf.fit(X1, y1, early_stopping_rounds=kwargs['early_stopping_rounds'], eval_metric='auc', eval_set=[(X2, y2)])
    if cv:
        clf=GridSearchCV(clf(), param_grid=args, cv=cv)
        clf.fit(x,y)
    else:
        clf = clf(**args)
        if 'cat_feature' in kwargs:
            clf.fit(x, y, kwargs['cat_feature'])
        else:
            clf.fit(x, y)
    return clf


def CatBoostReg_raise_fall(start_date, end_date, startegy_id, feature_days, selection_features, seed):
    CatBoost_para = {
        'learning_rate'   : .1,
        'max_depth'       : 6,
        'loss_function'   : 'RMSE',
        'nthread'         : 10,
        'n_estimators'    : 200,
        'random_seed'     : seed,
        'thread_count'    : 10,
    }
    trader = MLBiMergeRegTrader(None, start_date, end_date, feature_days, selection_features, startegy_id)

    X, Y = trader.preprocess(start_date, end_date)    
    trader.model = {
                    'rise_regressor': build_clf(CatBoostRegressor, X, Y['rise'], **CatBoost_para),
                    'fall_regressor': build_clf(CatBoostRegressor, X, Y['fall'], **CatBoost_para),
                    }
    return trader


def XGBClassifier_raise_fall(start_date, end_date, startegy_id, feature_days, selection_features, seed):
    xgb_para = {
        'colsample_bytree': .8,
        'gamma'           : .5,
        'learning_rate'   : .1,
        'max_depth'       : 5,
        'min_child_weight': 1,
        'n_estimators'    : 200,
        'random_state'    : seed,
        'subsample'       : .8,
        'nthread'         : 10,
    }
    trader = MLBiMergeTrader(None, start_date, end_date, feature_days, selection_features, startegy_id)

    X, Y = trader.preprocess(start_date, end_date)    
    trader.model = {
                    'rise_classifier': build_clf(XGBClassifier, X, Y['rise'], **xgb_para),
                    'fall_classifier': build_clf(XGBClassifier, X, Y['fall'], **xgb_para),
                    }
    return trader


def XGBRegressor_raise_fall(start_date, end_date, startegy_id, feature_days, selection_features, seed):
    xgb_para = {
        'colsample_bytree': .8,
        'gamma'           : .5,
        'learning_rate'   : .1,
        'max_depth'       : 5,
        'min_child_weight': 1,
        'n_estimators'    : 200,
        'random_state'    : seed,
        'subsample'       : .8,
        'nthread'         : 10,
        'reg_alpha'       :.75,
        'reg_lambd'       :.45,
    }
    trader = MLBiMergeRegTrader(None, start_date, end_date, feature_days, selection_features, startegy_id)

    X, Y = trader.preprocess(start_date, end_date)    
    trader.model = {
                    'rise_regressor': build_clf(XGBRegressor, X, Y['rise'], **xgb_para),
                    'fall_regressor': build_clf(XGBRegressor, X, Y['fall'], **xgb_para),
                    }
    return trader


def RandomForestRegressor_rasise_fall(start_date, end_date, startegy_id, feature_days, selection_features, seed):
    tree_param_grid={
        'min_sample_split': [3, 6, 9],
        'n_estimators': [10, 50, 100],
    }
    trader = MLBiMergeRegTrader(None, start_date, end_date, feature_days, selection_features, startegy_id)
    X, Y = trader.preprocess(start_date, end_date)    
    trader.model = {
                    'rise_regressor': build_clf(RandomForestRegressor, X, Y['rise'], 3, **tree_param_grid),
                    'fall_regressor': build_clf(RandomForestRegressor, X, Y['fall'], 3, **tree_param_grid),
                    }
    return trader