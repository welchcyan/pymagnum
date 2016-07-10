import pandas as pd
import line_algo as la


def spearman_corr(data):
    # type: (pd.DataFrame) -> pd.DataFrame
    _df = data.rank()
    result = _df['vol'].corr(_df['high'])
    return result


def alpha26(data, index=None, r_window=5, r_shift=1, r_rank=3):
    # type: (dict, list, int, int) -> dict

    """
     Alpha#26: (-1 * ts_max(correlation(ts_rank(volume, 5), ts_rank(high, 5), 5), 3))

    :param data: The set of {"symbos": dafa frame of symbols}
    :param index: The date index
    :param r_window: The evaluation window, default is 5
    :param r_shift: The evaluation shift, default is daily
    :return: The list of rank
    """
    dfd = dict()
    for symbol in data.keys():
        dfd[symbol] = la.rolling(data.get(symbol), spearman_corr, r_window=r_window, r_shift=r_shift)

    df_corr = pd.DataFrame(dfd, index=index)
    rankdf = df_corr.rank(1)
    iterdf = rankdf.iterrows()
    result = dict()
    for _ in range(len(rankdf)):
        row = next(iterdf)
        sorted_row = row[1].sort_values(ascending=False)[0:r_rank]
        result[sorted_row.name] = sorted_row.to_dict().keys()

    return result
