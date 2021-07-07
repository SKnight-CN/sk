import os
import numpy as np
import pandas as pd
import xlrd
from WindPy import w
import math
import time

def caculate_cuoquan(bond,jingjia):
    date = str(int(time.strftime("%Y%m%d", time.localtime())) - 1)
    tradedate = "tradeDate="+date
    inf = w.wss(bond, "couponrate2,ptmyear,latestpar",date)
    if inf.ErrorCode!=0:
        print("errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
        return
    lilv = (inf.Data)[0][0]
    shengyunianxian = (inf.Data)[1][0]
    mianzhi = (inf.Data)[2][0]
    times = math.ceil(shengyunianxian)
    yingjilixi = 100*lilv*(12-times)/12
    quanjia = jingjia+yingjilixi
    moni_jueduishouyi = ((lilv * times + mianzhi) / quanjia - 1) * 100
    return moni_jueduishouyi


def main():
    min = input("输入最低绝对收益率")
    shichang = pd.read_csv("市场跟踪.xlsx", encoding='gbk',usecols=['证券代码','证券简称','公司名称','绝对收益率','行权收益率','行权日','全价'])
    ruchigenzong = pd.DataFrame(columns=('证券代码','证券简称','公司名称','绝对收益率','行权收益率','行权日','全价','搓券净价','搓券全价','模拟绝对收益率','模拟行权收益率'))
    #bank = pd.DataFrame(pd.read_excel("银行间债券.xlsx", sheet_name="银行间数据全集"))
    #tradeins = pd.DataFrame(pd.read_excel("交易所债券 .xlsx", sheet_name="交易所数据全集"))
    # print(bank.iloc[:,0:2])
    #bank = bank.iloc[:, 0:2]
    #tradeins = tradeins.iloc[:, 0:2]
    for index, row in shichang.iterrows():
        if row['绝对收益率'] >= min:
            ruchigenzong = ruchigenzong.append(
                pd.DataFrame({'证券代码': [row['证券代码']], '证券简称': [row['证券简称']], '公司名称': [row['公司名称']],
                                '绝对收益率': [row['绝对收益率']],'行权收益率': [row['行权收益率']],'行权日': [row['行权日']],
                              '全价': [row['全价']],'搓券净价': [0],'搓券全价':[0],'模拟绝对收益率': [0],'模拟行权收益率':[0]}),
                ignore_index=True)

main()