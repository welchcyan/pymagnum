import numpy as np
import matplotlib.pyplot as plt

f = open('/Users/chenw13/Programs/quant/all_trading_data/index_data/sh000001.csv')

flist = [[line.split(',')[1], line.split(',')[5]] for line in f]

flist.reverse()

size = len(flist) - 1

x_axis = range(0, size)

index_value = np.array(flist[0:size])

index_val = np.array(index_value[:, 1], dtype=np.float64)

# Calculate the moving average of stock
def ma(ma_step, sourceList):
    i = 0
    ma_val = np.zeros(size, dtype=np.float64)
    ma_3 = 0.0
    for _ in sourceList:
        if i < ma_step - 1:
            ma_val[i] = sourceList[i]
        elif i == size:
            break
        else:
            j = i - ma_step + 1
            while i - j >= 0:
                ma_3 += sourceList[j]
                j += 1
            ma_3 /= ma_step
            ma_val[i] = ma_3
            ma_3 = 0.0
        i += 1
    return ma_val


ma_5 = ma(5, index_val)
ma_20 = ma(20, index_val)

plt.plot(x_axis, index_val)
plt.plot(x_axis, ma_5)
plt.plot(x_axis, ma_20, color='black')
plt.show()

f.close()
