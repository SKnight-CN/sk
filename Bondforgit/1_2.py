import os
import numpy as np
import pandas as pd
import xlrd
from WindPy import w
import math

ruchizhai = pd.DataFrame(pd.read_excel("入池债.xlsx"))
zhuti = input("输入入池主体\n")
name = input("简称\n")
ruchizhai = ruchizhai.append(pd.DataFrame({'入池主体': [zhuti], '简称': [name]}),
                ignore_index=True)
ruchizhai.to_excel("入池债.xlsx",index=False,header=True)
