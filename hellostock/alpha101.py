import numpy as np
import pandas as pd


def rolling(data, func, r_window=5, r_shift=1):
    # type: (pd.DataFrame, Any, int, int) -> list
    row_len = len(data)
    result = list()
    i = -1
    while i < row_len:
        if i+r_window+r_shift == row_len:
            break
        df = data.iloc[i+r_shift:i+r_window+r_shift, :]
        i += 1
        result.append(func(df))
    return result


def spearman_corr(data):
    # type: (pd.DataFrame) -> pd.DataFrame
    _df = data.rank()
    result = _df['vol'].corr(_df['high'])
    return result


def alpha26(data, index=None, r_window=5, r_shift=1, r_rank=3):
    # type: (dict, list, int, int, int) -> pd.DataFrame

    """
     Alpha#26: (-1 * ts_max(correlation( ts_rank(volume, 5), ts_rank(high, 5) , 5), 3))

    :param data: The set of {"symbos": dafa frame of symbols}
    :param index: The date index
    :param r_window: The evaluation window, default is 5
    :param r_shift: The evaluation shift, default is daily
    :param r_rank: The selected rank level of the universe
    :return: The DataFrame of selected symbols
    """
    dfd = dict()
    for symbol in data.keys():
        dfd[symbol] = rolling(data.get(symbol), spearman_corr, r_window=r_window, r_shift=r_shift)

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
