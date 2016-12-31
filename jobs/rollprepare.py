import sys
import os
import time

sys.path.append("../")

import hellostock.filehandler as fh
from multiprocessing import Pool
import pandas as pd

allsh = fh.load_dfs('/data/datacsv/sh_tran')

SH900912 = allsh['SH900912']

count = 0

for fpathe, dirs, fs in os.walk('.'):
    for f in fs:
        if  'xml'  in f.split('.'):
            print fpathe, f
            jfile = open(os.path.join(fpathe, f))
            for l in jfile:
                count += 1

print count

