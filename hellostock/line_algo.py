import numpy as np
import pandas as pd


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
