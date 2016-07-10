import pandas as pd


def alpha26(data):
    # type: (pd.DataFrame) -> pd.DataFrame
    """
    Alpha#26: (-1 * ts_max(correlation(ts_rank(volume, 5), ts_rank(high, 5), 5), 3))

    :param data: The DataFrame window
    :return: The Spearman rank correlation result DataFrame
    """
    _df = data.rank()
    result = _df['vol'].corr(_df['high'])
    return result
