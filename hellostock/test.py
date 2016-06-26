import numpy as np
import pandas as pd


def read_idx(fileurl):
    f = open(fileurl)
    flist = [[line.split(',')[1], line.split(',')[5]] for line in f]
    flist.reverse()
    size = len(flist) - 1
    x_axis_1 = range(0, size)
    index_value = np.array(flist[0:size])
    index_val_1 = np.array(index_value[:, 1], dtype=np.float64)
    f.close()
    return x_axis_1, index_val_1


x_axis, index_val = read_idx('/Users/chenw13/Programs/quant/all_trading_data/index_data/sh000001.csv')

x_axis2, index_val2 = read_idx('/Users/chenw13/Programs/quant/all_trading_data/index_data/sh000300.csv')

v1 = pd.Series(index_val)
v2 = pd.Series(index_val2)

v3 = pd.Series([1,2,3,4,5,6])
v4 = pd.Series([1,2,1,3,5,6])


print v1.corr(v2), v1.corr(v2, method="kendall"), v1.corr(v2, method="spearman")

print v3.corr(v4), v3.corr(v4, method="kendall"), v3.corr(v4, method="spearman")