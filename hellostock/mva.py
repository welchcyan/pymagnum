import pandas as pd
import line_algo as la


x_axis, index_val = la.read_idx('/Users/chenw13/Programs/quant/all_trading_data/index_data/sh000001.csv')

x_axis2, index_val2 = la.read_idx('/Users/chenw13/Programs/quant/all_trading_data/index_data/sh000300.csv')

v1 = pd.Series(index_val)
v2 = pd.Series(index_val2)

v3 = pd.Series([1,2,3,4,5,6])
v4 = pd.Series([1,2,1,3,5,6])


print v1.corr(v2), v1.corr(v2, method="kendall"), v1.corr(v2, method="spearman")

print v3.corr(v4), v3.corr(v4, method="kendall"), v3.corr(v4, method="spearman")


# D = pd.Series(index_val, x_axis)
#
# d_mva_1 = la.moving_average_1(5, index_val)
#
# print d_mva_1
#
# d_mva = la.moving_average_3(D, 5)
#
#
#
# print d_mva
#
# d_mva_2 = la.moving_average_2(index_val, 5)
#
# print d_mva_2

