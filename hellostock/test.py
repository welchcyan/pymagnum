import alpha101 as al
import pandas as pd
import filehandler as fh

# import matplotlib.pyplot as plot

# x_axis, index_val = la.read_idx('/Users/chenw13/Programs/quant/all_trading_data/index_data/sh000001.csv')
#
# x_axis2, index_val2 = la.read_idx('/Users/chenw13/Programs/quant/all_trading_data/index_data/sh000300.csv')
#
# v1 = pd.Series(index_val)
# v2 = pd.Series(index_val2)
#
# print v1.corr(v2), v1.corr(v2, method="kendall"), v1.corr(v2, method="spearman")


df0 = fh.read_stock('/Users/chenw13/Programs/quant/all_trading_data/stock_data/sh600000.csv')
df1 = fh.read_stock('/Users/chenw13/Programs/quant/all_trading_data/stock_data/sh600004.csv')
df2 = fh.read_stock('/Users/chenw13/Programs/quant/all_trading_data/stock_data/sh600005.csv')
df3 = fh.read_stock('/Users/chenw13/Programs/quant/all_trading_data/stock_data/sh600006.csv')
df4 = fh.read_stock('/Users/chenw13/Programs/quant/all_trading_data/stock_data/sh600007.csv')
df5 = fh.read_stock('/Users/chenw13/Programs/quant/all_trading_data/stock_data/sh600008.csv')
df6 = fh.read_stock('/Users/chenw13/Programs/quant/all_trading_data/stock_data/sh600009.csv')
df7 = fh.read_stock('/Users/chenw13/Programs/quant/all_trading_data/stock_data/sh600010.csv')
df8 = fh.read_stock('/Users/chenw13/Programs/quant/all_trading_data/stock_data/sh600011.csv')
df9 = fh.read_stock('/Users/chenw13/Programs/quant/all_trading_data/stock_data/sh600012.csv')
df10 = [df0, df1,df2,df3,df4,df5,df6,df7,df8,df9]

df = pd.DataFrame()
index1 = df5['date'].tolist()

dfd = dict()
dfd = {
    # 'sh600000': la.rolling(df0, spearman_corr),
    'sh600004': df1,
    # 'sh600005': la.rolling(df2, spearman_corr),
    # 'sh600006': la.rolling(df3, spearman_corr),
    'sh600007': df4,
    # 'sh600008': la.rolling(df5, spearman_corr),
    'sh600009': df6,
    # 'sh600010': la.rolling(df7, spearman_corr),
    'sh600011': df8,
    'sh600012': df9 }


df_corr = al.alpha26(dfd, index=index1, r_window=5, r_shift=1, r_rank=3)

# for _ in index1:
#     print df_corr[_]

print df_corr



# plot.plot(range(len(s1)), s1)
# plot.plot(range(len(s2)), s2)
# plot.plot(range(len(s3)), s3)
# plot.plot(range(len(s4)), s4)
#
# plot.show()
