from crawler import Crawler
import numpy as np
import pandas as pd
# import tushare as ts


cr = Crawler()

symbols = ["sh601006", "sz000001", "sz000002"]
rows = cr.get_latest_dailys(symbols)

rows_persist = np.array(rows)
df = pd.DataFrame(rows_persist)

df.to_csv("/Users/chenw13/Programs/test.csv")

# print ts.get_hist_data('601006')

