import sys

sys.path.append("../")

import hellostock.filehandler as fh

allsh = fh.read_stocks("/data/datacsv/sh")

print "A stocks number = ", len(allsh)

