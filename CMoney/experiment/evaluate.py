# third-party imports
import pickle
import numpy as np
import pandas as pd

# local imports
from data.gen_data import strategy


def daily_return_mean(df):
    '''
    每日報酬率平均值
    '''
    return df.daily_return.mean()


def daily_return_std(df):
    '''
    每日報酬的標準差
    '''
    return df.daily_return.std()


def calmar_ratio(df, MDD=None, Rp=None):
    '''
    Calmar Ratio: Rp / MDD
    Rp: Annual Profit, 年平均報酬
    '''
    if MDD is None:
        MDD = min(drawdown(df))
    if Rp is None:
        Rp = daily_return_mean(df)
    return Rp / -MDD


def drawdown(df):
    '''
    Max Drawdown, MDD, 最大連續虧損：損益創新高前的最大回檔幅度，可以知道最壞最壞的情況下可能虧損多少
    最長連續虧損：損益未再創新高的最長期間
    '''
    DD = [0]
    for PnL in df.PnL:
        d = DD[-1] + PnL
        if (d > 0):
            DD.append(0.0)
        else:
            DD.append(d)
    del DD[0]
    return DD


def information_ratio(df, Rb, Rp=None, std_Rp=None):
    '''
    Information Ratio: (Rp – Benchmark Annual Return(Rb)) / STD(Rp - Rb)
    '''
    if Rp is None:
        Rp = daily_return_mean(df)
    if std_Rp is None:
        std_Rp = daily_return_std(df)
    return (Rp - Rb) / (std_Rp - Rb)


def profit_factor(df):
    '''
    Profit Factor: AVG(profit)/AVG(loss)
    '''
    PnL = df.PnL
    return PnL.loc[PnL > 0] / PnL.loc[PnL]


def sharpe_ratio(df, Rf=(0.01 / 252), Rp=None, std_Rp=None):
    '''
    Sharpe Ratio: [(每日報酬率平均值- 無風險利率) / (每日報酬的標準差)]x (252平方根)
    Rf: Funding Cost, 資金成本，定存、投資其它指數、通貨膨脹等報酬率(以年為單位)，在計算時視為常數
    Rp: 每日報酬(%)=(今天資產淨值-昨天資產淨值)/昨天資產淨值
    '''
    if Rp is None:
        Rp = daily_return_mean(df)
    if std_Rp is None:
        std_Rp = daily_return_std(df)
    return ((Rp - Rf) / std_Rp) * pow(252, .5)


def win_rate(df):
    '''
    win rate = number of profit > 0 / total number of trades
    '''
    PnL = df.PnL	
    return PnL.loc[PnL > 0].count() / df.shape[0]


def trade_stock(products, start_data, end_data,
          data_path='./data/stocks', fee=.003, freq='m'):
    asset_sum = None
    for _, product in enumerate(products):
        with open(f'{data_path}/{product}.pkl', 'rb') as f:
            df = pickle.load(f).set_index('Date')

        asset = [1]
        df = df.loc[start_data:end_data]
        groups = df.groupby(pd.Grouper(freq=freq, level='Date'))
        for _, group in groups:
            group = group.reset_index()
            last_close = group['Close'].shift(1)
            last_close[0] = group.loc[0, 'Open']
            daily_rtn = np.append(asset[-1], group['Close'] / last_close)
            daily_rtn[-1] -= fee
            asset.extend(np.cumprod(daily_rtn)[1:])
        if asset_sum is None:
            asset_sum = np.array(asset)
        else:
            asset_sum += asset
    asset_sum = asset_sum / len(products)

    return pd.DataFrame({
        'asset': asset_sum[1:],
        'PnL': np.diff(asset_sum),
    })


def trade_stock(start_date, end_date, actions, strategy_id):
    fee = 1 # 美股交易手續費：0
    Daily_return = []
    PnL = []
    result = strategy[strategy_id][start_date:end_date]
    actions = actions[:len(result)]
    for action, trade_result in zip(actions, result.iterrows()):
        trade_result = trade_result[1]
        profit = 0
        if -1 == action: # put
            profit = trade_result['Put_result'] - fee
        elif 1 == action: # call
            profit = trade_result['Call_result'] - fee
        Daily_return.append(profit / trade_result['Cost'])
        PnL.append(profit)
        
    
    return pd.DataFrame({
        'Date': result.Date,
        'PnL': np.array(PnL), 
        'daily_return': np.array(Daily_return)
    })


def evaluate(df, Rf=(0.01 / 252), print=True):
    MDD = min(drawdown(df))
    Rp = daily_return_mean(df)
    std_Rp = daily_return_std(df)
    start = df.iloc[0].Date.strftime("%Y/%m/%d")
    end = df.iloc[-1].Date.strftime("%Y/%m/%d")
    return pd.DataFrame({
        'Date': f'{start}~{end}',
        'MDD': MDD,
        'Calmar_Ratio': calmar_ratio(df, MDD, Rp),
        'Sharpe_Ratio': sharpe_ratio(df, Rf),
        # 'Profit_Factor': profit_factor(df),
        'Win_Rate': win_rate(df),
    }, index = [0])
