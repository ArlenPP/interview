# output file
output file為dataframe的形式，以pickle的方式存在：
```
./output_apple_2020.pkl
```

# 訓練邏輯
1. 以2019年第一季為validation data挑選演算法、挑選特徵值、調整參數
2. 最終使用的資料集時間
    * train: 2013/1/1~2019/12/31
    * 演算法: CatBoostRegressor
    * 分別對作多、做空建立兩個模型，之後再做model ensemble產生結果

# 程式進入點
共有兩種進入方式
command line執行的方式比較方便做不同的實驗ex:換演算法，調參數等等
jupyter notebook的執行方式比較好demo
## command line進入方式
```
python3 experiment/run.py
```
## jupyter notebook進入方式
```
open interview.ipynb
```

# 特色
## 特徵工程
1. 結合了talib以及自定義的feature,自定義feature寫在data/feature.py
2. 可以快速抽換不同的交易策略結合n天前的feature，n天也可以快速調整，詳見data/gen_data.py中的build_XY
## 快速嘗試不同實驗
1. 透過自定義的Class Trader將不論事回歸或分類甚至是深度學習的模型，都可以擁有相同的predict介面
2. 透過Trader.py以及exp.py的結合，可以快速嘗試不同的演算法，以及不同的參數
## 回測及分析
1. evaluate.py中的evaluate function可以將不同交易結果快速產生報告

# 交易策略
    * 進/出場點皆為新/平倉單日開盤價（預掛）
    * 持倉最大單位：1
    * 交易手續費：預設為0,可在evaluate.py中修改
    * 共有三種交易策略：
        1. 新倉t+1天後平倉
        2. 新倉t+2天後平倉
        3. 新倉t+2天後平倉
