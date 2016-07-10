import random
import numpy as np


def mc_pi(num1):
    count = 0
    for i in range(1, num1 + 1):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        if pow(x, 2) + pow(y, 2) < 1:
            count += 1
    return 4.0 * count / num1


def liner_approxmate():
    ymax = 0
    yf = lambda x: 200 * np.sin(x) * np.exp(-0.05 * x)
    num = 10000
    for m in range(1, num + 1):
        x0 = random.uniform(-2, 2)
        if yf(x0) > ymax:
            ymax = yf(x0)
            xmax = x0

    print xmax, ymax
