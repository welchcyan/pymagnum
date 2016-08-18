def worker(unit):
    """
    Use pd.DataFrame join to prepare the transformation
    :type unit: pd.DataFrame
    """
    print 'Process Starting...'
    symbol = unit['symbol'][0]
    data = {'date': all_index,
            'symbol': pd.Series(np.array([symbol] * all_index.size), index=all_index),
            'open': pd.Series(np.linspace(0, 0, num=all_index.size), index=all_index, dtype=float),
            'high': pd.Series(np.linspace(0, 0, num=all_index.size), index=all_index, dtype=float),
            'low': pd.Series(np.linspace(0, 0, num=all_index.size), index=all_index, dtype=float),
            'close': pd.Series(np.linspace(0, 0, num=all_index.size), index=all_index, dtype=float),
            'vol': pd.Series(np.linspace(0, 0, num=all_index.size), index=all_index, dtype=float)
            }
    col = ['date', 'symbol', 'open', 'high', 'low', 'close', 'vol']
    empty_frame = pd.DataFrame(data, index=all_index, columns=col)
    all_transformed[symbol] = empty_frame.join(unit, on='date', how='left')
    print 'Exiting...'
    pass