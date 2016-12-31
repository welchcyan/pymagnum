import sys
import os
import time

sys.path.append("../")

import hellostock.filehandler as fh
from multiprocessing import Pool
import pandas as pd


allsh = dict()
all_index = pd.DataFrame()
all_transformed = dict()


def load_data():
    global allsh, all_index
    # read all sh stocks into a dict
    allsh = fh.read_stocks("/Users/chenw13/Programs/quant/datacsv/sz_orig")

    print "A stocks number = ", len(allsh)

    # find the max trade days to regularize the all dataset
    maxdays = 0
    tradedays = 0
    tradesymbol = ""

    for k in allsh:
        tradedays = len(allsh[k])
        if maxdays < tradedays:
            maxdays = tradedays
            tradesymbol = k

    print tradesymbol, maxdays

    # Find the A index date as the dataframe index
    all_index = fh.read_stock("/Users/chenw13/Programs/quant/datacsv/sz_idx/SZ000001.csv").date


def worker(unit, container):
    """
    Use interate to prepare the transformation

    :type unit: pd.DataFrame
    """
    symbol = unit['symbol'][0]
    print "Start to process symbol", symbol, ".................."
    start = time.time()
    all_shlist = list()
    for da in all_index:
        if da in unit['date']:
            cell = unit[da:da]
            all_shlist.append((cell.date[0], cell.symbol[0], cell.open[0], cell.high[0], cell.low[0], cell.close[0], cell.vol[0]))
        else:
            all_shlist.append((da, symbol, 0.0, 0.0, 0.0, 0.0, 0.0))
    col = ['date', 'symbol', 'open', 'high', 'low', 'close', 'vol']
    resultdf = pd.DataFrame.from_records(all_shlist, index=all_index, columns=col)
    resultdf.to_csv(os.path.join('/Users/chenw13/Programs/quant/datacsv/sz_tran/', symbol), header=True, index=True, col=col, index_label='idx')
    end = time.time()
    print "Symbol", symbol, "processed, result len=", len(resultdf), " process time = ", end - start
    container[symbol] = resultdf
    return resultdf


print "STEP 1 =============================================="
print "Start to parsing original data"
start = time.time()
load_data()
end = time.time()
print "Parsing original data end, time taken=", end - start
print "STEP 1 =============================================="


print "STEP 2 =============================================="
print "Start to parsing original data"
# multiprocess the whole sh stocks
pool = Pool(processes=20)

# prepare the transformed dict
start = time.time()
for j in allsh:
    pool.apply_async(worker, (allsh[j], all_transformed, ))

pool.close()
pool.join()
end = time.time()
print "Parsing original data end, time taken=", end - start
print "STEP 2 =============================================="

# new_frame = pd.read_csv('/Users/chenw13/Programs/quant/datacsv/sh_tran/SH900916', parse_dates=True, index_col=0)

# haha = fh.load_dfs('/Users/chenw13/Programs/quant/datacsv/sz_tran/')
