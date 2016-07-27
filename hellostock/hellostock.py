import filehandler as fh
import line_algo as la
import matplotlib.pyplot as plt


def plot():
    r = fh.read_stock('/Users/chenw13/Programs/quant/all_trading_data/stock_data/sh600000.csv')
    daily = r.get('close').tolist()
    ma_5 = la.moving_average_3(r.get('close'), 5)
    ma_20 = la.moving_average_3(r.get('close'), 20)
    index_val = r['date'].tolist()
    x_axis = range(0, len(index_val))

    plt.plot(x_axis, daily, color='green')
    plt.plot(x_axis, ma_5, color='blue')
    plt.plot(x_axis, ma_20, color='black')
    plt.show()
