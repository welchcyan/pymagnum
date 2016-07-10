import numpy as np
import pandas as pd


def read_idx(fileurl):
    # type: (str) -> list, ndarray
    f = open(fileurl)
    flist = [[line.split(',')[1], line.split(',')[5]] for line in f]
    flist.reverse()
    size = len(flist) - 1
    x_axis = range(0, size)
    index_value = np.array(flist[0:size])
    index_val = np.array(index_value[:, 1], dtype=np.float64)
    f.close()
    return x_axis, index_val


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


def read_stock(fileurl):
    # type: (str) -> pd.DataFrame
    f = open(fileurl)
    flist = []
    f.next()
    for line in f:
        line_val = line.split(',')
        flist.append(
            [line_val[1], line_val[0], line_val[2], line_val[3], line_val[4], line_val[5], line_val[7]])
    flist.reverse()
    flist = np.array(flist)
    ind = np.array(flist[:, 0], dtype=pd.Timestamp)
    data = {'date': pd.Series(flist[:, 0], index=ind), 'symbol': pd.Series(flist[:, 1], index=ind),
            'open': pd.Series(flist[:, 2], index=ind), 'high': pd.Series(flist[:, 3], index=ind),
            'low': pd.Series(flist[:, 4], index=ind), 'close': pd.Series(flist[:, 5], index=ind),
            'vol': pd.Series(flist[:, 6], index=ind)
            }
    col = ['date', 'symbol', 'open', 'high', 'low', 'close', 'vol']
    stock_frame = pd.DataFrame(data, index=ind, columns=col)
    f.close()
    return stock_frame


def moving_average_1(ma_step, sourcelist):
    i = 0
    size = len(sourcelist)
    ma_vector = np.zeros(size, dtype=np.float64)
    ma_window = 0.0
    for _ in sourcelist:
        if i < ma_step - 1:
            ma_vector[i] = sourcelist[i]
        elif i == size:
            break
        else:
            j = i - ma_step + 1
            while i - j >= 0:
                ma_window += sourcelist[j]
                j += 1
            ma_window /= ma_step
            ma_vector[i] = ma_window
            ma_window = 0.0
        i += 1
    return ma_vector


def moving_average_2(x, n, method='simple'):
    # type: (list, int, basestring) -> DataFrame
    """
    compute an n period moving average.

    type is 'simple' | 'exponential'

    """
    x = np.asarray(x)
    if method == 'simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))

    weights /= weights.sum()

    a = np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a


def moving_average_3(s, t):
    # type: (list, int) -> Window
    s = pd.Series(s)
    d_mva = s.rolling(window=t, center=False).mean()
    return d_mva
