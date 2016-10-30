# coding=utf-8
import numpy as np
import pandas as pd
import sys
from collections import defaultdict

'''
Alpha101

Terms:

abs(x), log(x), sign(x) = standard definitions;
same for the operators “+”, “-”, “*”, “/”, “>”, “<”, “==”, “||”, “x ? y : z”
rank(x) = cross-sectional rank
delay(x, d) = value of x d days ago
correlation(x, y, d) = time-serial correlation of x and y for the past d days
covariance(x, y, d) = time-serial covariance of x and y for the past d days
scale(x, a) = rescaled x such that sum(abs(x)) = a (the default is a = 1)
delta(x, d) = today’s value of x minus the value of x d days ago
signedpower(x, a) = x^a
decay_linear(x, d) = weighted moving average over the past d days with linearly decaying weights d, d – 1, ..., 1
(rescaled to sum up to 1)
indneutralize(x, g) = x cross-sectionally neutralized against groups g (subindustries, industries, sectors, etc.),
i.e., x is cross-sectionally demeaned within each group g
ts_{O}(x, d) = operator O applied across the time-series for the past d days; non-integer number of days d is converted
to floor(d)
ts_min(x, d) = time-series min over the past d days
ts_max(x, d) = time-series max over the past d days
ts_argmax(x, d) = which day ts_max(x, d) occurred on
ts_argmin(x, d) = which day ts_min(x, d) occurred on
ts_rank(x, d) = time-series rank in the past d days
min(x, d) = ts_min(x, d)
max(x, d) = ts_max(x, d)
sum(x, d) = time-series sum over the past d days
product(x, d) = time-series product over the past d days
stddev(x, d) = moving time-series standard deviation over the past d days

returns = daily close-to-close returns
open, close, high, low, volume = standard definitions for daily price and volume data
vwap = daily volume-weighted average price
cap = market cap
adv{d} = average daily dollar volume for the past d days
IndClass = a generic placeholder for a binary industry classification such as GICS, BICS, NAICS, SIC, etc.,
in indneutralize(x, IndClass.level), where level = sector, industry, subindustry, etc. Multiple IndClass in the
same alpha need not correspond to the same industry classification.

'''


def rolling(data, r_window, r_shift, func, **kwargs):
    # type: (pd.DataFrame, int, int, Any, Any) -> list
    row_len = len(data)
    result = list()
    i = -1
    while i < row_len:
        if i + r_window + r_shift >= row_len:
            result.append(func(data, **kwargs))
            return result
        df = data.iloc[i + r_shift:i + r_window + r_shift, :]
        i += 1
        result.append(func(df, **kwargs))
    return result


def projection(data, colname):
    # type: (dict, str) -> pd.DataFrame

    """

    :rtype: dfd:
    :param data:
    :param colname:
    """
    dfd = pd.DataFrame()
    for k, v in data.items():
        dfd[k] = v[colname]

    return dfd


def spearman_corr(data, **kwargs):
    # type: (pd.DataFrame, Any) -> pd.DataFrame
    _df = data.rank()
    result = _df[kwargs['left']].corr(_df[kwargs['right']])
    return result


def alpha26(data, index=None, r_window=5, r_shift=1, r_rank=3):
    # type: (dict, list, int, int, int) -> pd.DataFrame

    """
     Alpha#26: (-1 * ts_max(correlation( ts_rank(volume, 5), ts_rank(high, 5) , 5), 3))

    :param data: The dict of dataframes {key=symbolID,value=dataframe}
    :param index: The date index
    :param r_window: The evaluation window, default is 5
    :param r_shift: The evaluation shift, default is daily
    :param r_rank: The selected rank level of the universe
    :return: The DataFrame of selected symbols
    """
    dfd = dict()
    for k, v in data.items():
        dfd[k] = rolling(v, r_window, r_shift, spearman_corr, **{'left': 'vol', 'right': 'high'})

    df_corr = pd.DataFrame(dfd, index=index)
    rankdf = df_corr.rank(1)
    iterdf = rankdf.iterrows()
    _index = list()
    resultdict = dict()
    _cols = range(0, r_rank)
    for i in _cols:
        resultdict[i] = list()
    for _ in range(len(rankdf)):
        row = next(iterdf)
        sorted_row = row[1].sort_values(ascending=False)[0:r_rank]
        _index.append(sorted_row.name)
        keys = sorted_row.to_dict().keys()
        for i in _cols:
            resultdict[i].append(keys[i])
    resultdf = pd.DataFrame(resultdict, index=_index, columns=_cols)
    return resultdf


def compare_vol_close(data, **kwargs):
    # type: (pd.DataFrame, Any) -> int
    """
    comprator of the vol and close
    :param data: dataframe
    :param kwargs: any
    """
    resultdict = dict()
    resultdict['symbol'] = data['symbol'][0]
    history_close_max = kwargs['high']
    resultdict['hismax'] = history_close_max
    window_size = len(data) - 1
    current_close = data[kwargs['right']][window_size]
    if current_close >= history_close_max:
        window_vol_mean = data[window_size - kwargs['shift']:window_size - 1][kwargs['left']].mean()
        if window_vol_mean == 0.0:
            window_vol_mean = 0.1
        print "mean:" , window_vol_mean
        current_vol = data[kwargs['left']][window_size]
        print "current:", current_vol
        ratio = (current_vol - window_vol_mean) / window_vol_mean
        print "ratio:", ratio
        if ratio >= kwargs['threshold']:
            resultdict['ratio'] = ratio
        else:
            resultdict['ratio'] = 0
    else:
        resultdict['ratio'] = 0
    return resultdict


def alpha_zhangtao(data, index=None, r_window=sys.maxint, r_shift=3, r_rank=10, threshold = 0.5):
    # type: (dict, list, int, int, int, int) -> dict
    """
    A simple rule to find potential stock universe
    The close price higher than the highest forever or the highest in r_window
    and at the same time its volume higher than last 3 days average volume

    :return:
    :param data: The dict of dataframes {key=symbolID,value=dataframe}
    :param index: The data index
    :param r_window: The evaluation window, shoud be as long as possible, but also can be multiply of 1 year
    :param r_shift: The evaluate window for volume increase, default is 3 days
    :param r_rank: filter out the result, default is 10
    :param r_vol_increase: the volume increasement, default is 50%
    """
    dfd = dict()
    for k, v in data.items():
        history_close_max = v['close'].max()
        dfd[k] = rolling(v, r_window, r_shift, compare_vol_close, **{'left': 'vol', 'right': 'close', 'high':history_close_max, 'threshold':threshold, 'shift':r_shift})

    symbol_list = list()
    ratio_list = list()
    max_list = list()
    for k, v in dfd.items():
        symbol_list.append(k)
        ratio_list.append(v[0]['ratio'])
        max_list.append(v[0]['hismax'])
    symbol_series = pd.Series(np.array(symbol_list), symbol_list, dtype=str)
    ratio_series = pd.Series(np.array(ratio_list), symbol_list, dtype=float)
    max_series = pd.Series(np.array(max_list), symbol_list, dtype=float)

    ind = np.array(symbol_list, dtype=str)
    data = {'symbol': symbol_series,
            'hismax': max_series,
            'ratio': ratio_series
            }
    col = ['symbol', 'hismax', 'ratio']
    stock_frame = pd.DataFrame(data, index=ind, columns=col)
    return stock_frame


def alpha2(data, index=None, r_window=6, r_shift=1, r1_rank=2, r2_rank=6):
    # type: (dict, list, int, int, int) -> dict()

    """
     Alpha#2: (-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))

    :param data: The dict of dataframes {key=symbolID,value=dataframe}
    :param index: The date index
    :param r_window: The evaluation window, default is 6
    :param r_shift: The evaluation shift, default is daily
    :param r1_rank: The selected rank level of the vol
    :param r2_rank: The correlation window
    :return: The DataFrame of selected symbols
    """
    dfd = dict()
    for k, v in data.items():
        newframe = pd.DataFrame()
        v1 = newframe.assign(logv=np.log2(v['vol']))
        v2 = v1.assign(spread=(v['close'] - v['open']) / v['open'])
        dfd[k] = v2

    difflist = dict()
    for k, v in dfd.items():
        difflist[k] = list()
        for i in range(0, len(dfd[k])):
            if i + r1_rank == len(dfd[k]):
                break
            else:
                difflist[k].append(v['logv'][i] - v['logv'][i + r1_rank])

    for i in range(0, r1_rank):
        for k, v in difflist.items():
            v.append(None)
    #construct delta, spread data frame done

    dfr = dict()
    for k, v in dfd.items():
        v1 = v.assign(delta=difflist[k])
        dfr[k] = v1
        # dfr[k] = rolling(v1, r_window, r_shift, spearman_corr, **{'left': 'delta', 'right': 'spread'})

    delta_frame = projection(dfr, 'delta')
    spread_frame = projection(dfr, 'spread')

    print delta_frame.rank(1).head(6)
    print spread_frame.rank(1).head(6)

    return dfr
    # resultdf = pd.DataFrame(dfr, index=index)
    # return resultdf
    pass
    #     dfd[k] = rolling(v, r_window, r_shift, spearman_corr, **{'left': 'vol', 'right': 'high'})
    #
    # df_corr = pd.DataFrame(dfd, index=index)
    # rankdf = df_corr.rank(1)
    # iterdf = rankdf.iterrows()
    # _index = list()
    # resultdict = dict()
    # _cols = range(0, r2_rank)
    # for i in _cols:
    #     resultdict[i] = list()
    # for _ in range(len(rankdf)):
    #     row = next(iterdf)
    #     sorted_row = row[1].sort_values(ascending=False)[0:r2_rank]
    #     _index.append(sorted_row.name)
    #     keys = sorted_row.to_dict().keys()
    #     for i in _cols:
    #         resultdict[i].append(keys[i])
    # resultdf = pd.DataFrame(resultdict, index=_index, columns=_cols)
    # return resultdf
