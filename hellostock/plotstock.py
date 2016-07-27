import filehandler as fh
import line_algo as la
import talib as ta
import numpy as np
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt


def plotstock(filepath):
    """

    :type filepath: str
    """
    r = fh.read_stock(filepath)
    daily = r.get('close').tolist()
    index_val = r['date'].tolist()
    x_axis = range(0, len(index_val))

    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    textsize = 9
    left, width = 0.1, 0.8
    rect1 = [left, 0.7, width, 0.2]
    rect2 = [left, 0.3, width, 0.4]
    rect3 = [left, 0.1, width, 0.2]

    fig = plt.figure(facecolor='white')
    axescolor = '#f6f6f6'  # the axes background color

    ax1 = fig.add_axes(rect1, axisbg=axescolor)  # left, bottom, width, height
    ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
    ax2t = ax2.twinx()
    ax3 = fig.add_axes(rect3, axisbg=axescolor, sharex=ax1)

    # plot the relative strength indicator
    prices = np.array(daily, dtype=float)
    rsi = ta.RSI(prices)
    fillcolor = 'darkgoldenrod'

    ax1.plot(x_axis, rsi, color=fillcolor)
    ax1.axhline(70, color=fillcolor)
    ax1.axhline(30, color=fillcolor)
    ax1.fill_between(x_axis, rsi, 70, where=(rsi >= 70), facecolor=fillcolor, edgecolor=fillcolor)
    ax1.fill_between(x_axis, rsi, 30, where=(rsi <= 30), facecolor=fillcolor, edgecolor=fillcolor)
    ax1.text(0.6, 0.9, '>70 = overbought', va='top', transform=ax1.transAxes, fontsize=textsize)
    ax1.text(0.6, 0.1, '<30 = oversold', transform=ax1.transAxes, fontsize=textsize)
    ax1.set_ylim(0, 100)
    ax1.set_yticks([30, 70])
    ax1.text(0.025, 0.95, 'RSI (14)', va='top', transform=ax1.transAxes, fontsize=textsize)
    ax1.set_title('%s daily' % filepath[filepath.rindex('/')+1:filepath.index('.')])

    # plot the price and volume data
    low = r.low
    high = r.high

    deltas = np.zeros_like(prices)
    deltas[1:] = np.diff(prices)
    up = deltas > 0
    # ax2.vlines(r.date[up], low[up], high[up], color='black', label='_nolegend_')
    # ax2.vlines(r.date[~up], low[~up], high[~up], color='black', label='_nolegend_')
    ma5 = la.moving_average_3(r.get('close'), 5)
    ma20 = la.moving_average_3(r.get('close'), 20)

    linedaily, = ax2.plot(x_axis, daily, color='black', lw=1, label='Daily')
    linema20, = ax2.plot(x_axis, ma5, color='blue', lw=0.5, label='MA (20)')
    linema200, = ax2.plot(x_axis, ma20, color='red', lw=0.5, label='MA (200)')

    # last = r[-1]
    # s = '%s O:%1.2f H:%1.2f L:%1.2f C:%1.2f, V:%1.1fM Chg:%+1.2f' % (
    #     today.strftime('%d-%b-%Y'),
    #     last.open, last.high,
    #     last.low, last.close,
    #     last.volume*1e-6,
    #     last.close - last.open)
    # t4 = ax2.text(0.3, 0.9, s, transform=ax2.transAxes, fontsize=textsize)
    #
    # props = font_manager.FontProperties(size=10)
    # leg = ax2.legend(loc='center left', shadow=True, fancybox=True, prop=props)
    # leg.get_frame().set_alpha(0.5)

    volume = (r.close * r.vol) / 1e6  # dollar volume in millions
    vmax = volume.max()
    poly = ax2t.fill_between(x_axis, volume, 0, label='Volume', facecolor=fillcolor, edgecolor=fillcolor)
    ax2t.set_ylim(0, 5 * vmax)
    ax2t.set_yticks([])

    # compute the MACD indicator
    fillcolor = 'darkslategrey'
    nslow = 26
    nfast = 12
    nema = 9
    emaslow, emafast, macd = ta.MACD(prices, fastperiod=nfast, slowperiod=nslow)
    ema9 = ta.EMA(macd, nema)
    ax3.plot(x_axis, macd, color='black', lw=2)
    ax3.plot(x_axis, ema9, color='blue', lw=1)
    ax3.fill_between(x_axis, macd - ema9, 0, alpha=0.5, facecolor=fillcolor, edgecolor=fillcolor)
    ax3.text(0.025, 0.95, 'MACD (%d, %d, %d)' % (nfast, nslow, nema), va='top', transform=ax3.transAxes,
             fontsize=textsize)

    # ax3.set_yticks([])
    # turn off upper axis tick labels, rotate the lower ones, etc
    for ax in ax1, ax2, ax2t, ax3:
        if ax != ax3:
            for label in ax.get_xticklabels():
                label.set_visible(False)
        else:
            for label in ax.get_xticklabels():
                label.set_rotation(30)
                label.set_horizontalalignment('right')

        ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')

    class MyLocator(mticker.MaxNLocator):
        def __init__(self, *args, **kwargs):
            mticker.MaxNLocator.__init__(self, *args, **kwargs)

        def __call__(self, *args, **kwargs):
            return mticker.MaxNLocator.__call__(self, *args, **kwargs)

    # at most 5 ticks, pruning the upper and lower so they don't overlap
    # with other ticks
    # ax2.yaxis.set_major_locator(mticker.MaxNLocator(5, prune='both'))
    # ax3.yaxis.set_major_locator(mticker.MaxNLocator(5, prune='both'))

    ax2.yaxis.set_major_locator(MyLocator(5, prune='both'))
    ax3.yaxis.set_major_locator(MyLocator(5, prune='both'))

    # plt.plot(x_axis, daily, color='green')
    # plt.plot(x_axis, ma_5, color='blue')
    # plt.plot(x_axis, ma_20, color='black')
    plt.show()
