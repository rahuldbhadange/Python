#!/bin/python3

import math
import os
import random
import re
import sys




# Complete the 'restock' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_ARRAY itemCount
#  2. INTEGER target
#

def restock(itemCount, target):
    # Write your code here
    # print(itemCount,type(itemCount), target, type(target))
    units = sum(itemCount)
    if units < target:
        additional_units = target - units
        return additional_units
    else:
        unit = 0
        for unit in itemCount:
            print("before", unit)
            unit = unit + unit
            print("after", unit)
            if unit > target:
                print("final",unit)
                additional_units = unit - target
                return additional_units




if __name__ == '__main__':
    restock([174, 156, 167,138,187,111,196,140,100,156], 1522)
