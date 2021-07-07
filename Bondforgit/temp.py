import datetime
import os
import numpy as np
import pandas as pd
import xlrd
from WindPy import w
import math
import time

def chuliriqi():
    everything = pd.read_csv("bonds.csv")
    for index, row in everything.iterrows():
        temp = list(row['到期日期'])
        ind = []
        for i, ch in enumerate(temp):
            if ch == '/':
                ind.append(i)
        temp.pop(ind[0])
        temp.pop(ind[1] - 1)
        temp = ''.join(temp)
        temp = datetime.datetime.strptime(temp, '%Y%m%d').date()
        temp = str(temp)
        temp = list(temp)
        for i, ch in enumerate(temp):
            if ch == '-':
                ind.append(i)
        temp.pop(ind[2])
        temp.pop(ind[3] - 1)
        temp = ''.join(temp)
        everything.iat[index, 3] = temp
    everything.to_csv("bonds.csv", encoding='utf_8_sig', index=False, header=True)

def test():
    w.start()
    everything = pd.read_excel("blank.xlsx")
    date = "date=" + str(
        time.strftime("%Y-%m-%d", time.localtime())) + ";sectorid=1000008620000000;field=wind_code,sec_name"
    # 从wind提取一个月内上市得债券
    inf = w.wset("sectorconstituent", date)
    if inf.ErrorCode != 0:
        print("errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrror")
    new_bonds_codes = inf.Data[0][0:5]
    new_bonds_names = inf.Data[1][0:5]
    i = 0
    for index, bondcode in enumerate(new_bonds_codes):
        daoqiri = (w.wss(bondcode, "maturitydate").Data)[0]
        daoqidate = str(daoqiri[0].year) + '-' + str(daoqiri[0].month) + '-' + str(daoqiri[0].day)
        temp = list(daoqidate)
        ind = []
        for i, ch in enumerate(temp):
            if ch == '-':
                ind.append(i)
        temp.pop(ind[0])
        temp.pop(ind[1] - 1)
        temp = ''.join(temp)
        temp = datetime.datetime.strptime(temp, '%Y%m%d').date()
        temp = str(temp)
        temp = list(temp)
        for i, ch in enumerate(temp):
            if ch == '-':
                ind.append(i)
        temp.pop(ind[2])
        temp.pop(ind[3] - 1)
        temp = ''.join(temp)
        everything = everything.append(
            pd.DataFrame({'证券代码': [bondcode], '证券简称': [new_bonds_names[index]], '到期日期': [temp]}),
            ignore_index=True)
    print(everything)

test()