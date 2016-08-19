import os
import numpy as np
import pandas as pd


def read_idx(fileurl):
    # type: (str) -> list, ndarray
    f = open(fileurl)
    flist = [[line.split(',')[1], line.split(',')[5]] for line in f]
    # flist.reverse()
    size = len(flist) - 1
    x_axis = range(0, size)
    index_value = np.array(flist[0:size])
    index_val = np.array(index_value[:, 1], dtype=np.float64)
    f.close()
    return x_axis, index_val


def read_stock(fileurl):
    # type: (str) -> pd.DataFrame
    f = open(fileurl)
    flist = []
    f.next()
    for line in f:
        line_val = line.split(',')
        flist.append(
            [line_val[1], line_val[0], line_val[2], line_val[3], line_val[4], line_val[5], line_val[7]])
    # flist.reverse()
    flist = np.array(flist)
    ind = np.array(flist[:, 0], dtype=pd.Timestamp)
    data = {'date': pd.Series(flist[:, 0], index=ind, dtype=pd.Timestamp), 'symbol': pd.Series(flist[:, 1], index=ind),
            'open': pd.Series(flist[:, 2], index=ind, dtype=float),
            'high': pd.Series(flist[:, 3], index=ind, dtype=float),
            'low': pd.Series(flist[:, 4], index=ind, dtype=float),
            'close': pd.Series(flist[:, 5], index=ind, dtype=float),
            'vol': pd.Series(flist[:, 6], index=ind, dtype=float)
            }
    col = ['date', 'symbol', 'open', 'high', 'low', 'close', 'vol']
    stock_frame = pd.DataFrame(data, index=ind, columns=col)
    f.close()
    return stock_frame


def read_stocks(dir_url):
    # type: (str) -> dict

    """
    Read all stock files under dir_url

    :type dir_url: str
    :rtype: object a dict contains key:symbol name, value:DataFrame
    """
    _dfd = dict()
    for fpathe, dirs, fs in os.walk(dir_url):
        for f in fs:
            _dfd[f.split('.')[0]] = read_stock(os.path.join(fpathe, f))
    return _dfd


def load_dfs(dir_url):
    # type: (str) -> dict

    """
    Load all transformed stock data persist by pd.to_csv

    :type dir_url: str
    :rtype: object a dict contains key:symbol name, value:DataFrame
    """
    _dfd = dict()
    for fpathe, dirs, fs in os.walk(dir_url):
        for f in fs:
            _dfd[f] = pd.read_csv(os.path.join(fpathe, f), parse_dates=True, index_col=0)

    return _dfd


def load_df(file_url):
    # type: (str) -> pd.DataFrame

    """
    Load single transformed stock data persist by pd.to_csv

    :type file_url: str
    :rtype: df: pd.DataFrame
    """
    df = pd.read_csv(file_url, parse_dates=True, index_col=0)

    return df

