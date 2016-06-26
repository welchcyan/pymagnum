from crawler import Crawler
# import tushare as ts


cr = Crawler()
# row = cr.get_latest_daily("sh601006")

# print row

symbols = ["sh601006", "sz000001", "sz000002"]
rows = cr.get_latest_dailys(symbols)

print rows

# print ts.get_hist_data('601006')

