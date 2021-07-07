import os
import numpy as np
import pandas as pd
import xlrd
from WindPy import w
import math
import time

def update_bond():
    everything = pd.read_csv("bonds.xlsx", encoding='gbk')
    date = "date=" + str(int(time.strftime("%Y-%m-%d", time.localtime()))) + ";sectorid=1000008620000000;field=wind_code,sec_name"
    inf = w.wset("sectorconstituent",date)
    if inf.ErrorCode==0:
        print("errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrror")
        return
    new_bonds = inf.Data
    for bond in new_bonds:
        daoqiri = (w.wss("136670.SH", "maturitydate").Data)[0]
        for index,ch in enumerate(daoqiri):
            if ch == '/':
                daoqiri[index]='-'
        everything = everything.append(
            pd.DataFrame({'证券代码': [bond[0][0]], '证券简称': [bond[1][0]], '到期日期':[daoqiri]}),
            ignore_index=True)
    #去重
    everything.drop_duplicates(subset='证券代码',keep='last',inplace=True)
    #按到期日近到远排序
    everything.sort_values('到期日期',inplace=True)
    everything.to_excel("bonds.xlsx", index=False, header=True)


def find_product(tradeplace,shichang):
    date = str(int(time.strftime("%Y%m%d", time.localtime())) - 1)
    print(date)
    tradedates = "tradeDate=" + str(date) + ";date=" + str(date) + ";type=All;cycle=D"
    for index, row in tradeplace.iterrows():
        # YTM_ifexe-行权收益率,dirtyprice-收盘全价,nxoptiondate-下一行权日,volume-成交量,amt-成交额,latestpar-债券最新面值，couponrate3-票面利率，pymyear-剩余年限
        # termifexericse-行权剩余年限
        # w.wss(row[0], "YTM_ifexe,dirtyprice,nxoptiondate,volume,amt,latestpar,couponrate3,ptmyear,termifexercise"
        #      , "tradeDate=20210605;date=20210604;type=C;cycle=D")
        tag = 0
        print(index)
        inf = (w.wss(row[0], "YTM_ifexe,dirtyprice,nxoptiondate,volume,amt,fund_parvalue,couponrate2,ptmyear,termifexercise",
                     tradedates)).Data
        xingquanshouyi = float(''.join([str(x) for x in inf[0]]))
        shoupanquanjia = float(''.join([str(x) for x in inf[1]]))
        xingquanri = float(''.join([str(x) for x in inf[2]]))
        chengjiaoliang = float(''.join([str(x) for x in inf[3]]))
        chengjiaoe = float(''.join([str(x) for x in inf[4]]))
        mianzhi = float(''.join([str(x) for x in inf[5]]))
        piaomianlilv = float(''.join([str(x) for x in inf[6]]))
        rest_date = float(''.join([str(x) for x in inf[7]]))
        xingquan = float(''.join([str(x) for x in inf[8]]))
        # 判断行权收益或者绝对收益大于10
        if xingquan != xingquan:
            times = math.ceil(rest_date)
        else:
            times = math.ceil(xingquan)
        jueduishouyi = ((piaomianlilv * times + mianzhi) / shoupanquanjia - 1) * 100
        if xingquanshouyi != xingquanshouyi:
            if xingquanshouyi > 10:
                tag = 1
        if not tag:
            if jueduishouyi > 10:
                tag = 1
        if tag:
            print(inf)
            print(jueduishouyi)
            date = list(((w.wss(row[0], "nxoptiondate", tradedates)).Data)[0])
            if date[0]!=None:
                date = list(date[0])
                date[4]=''
                date[7]=''
                date = ''.join(date)
            else:
                date=0
            shichang = shichang.append(
                pd.DataFrame({'证券代码': [row[0]], '证券简称': [row[1]], '公司名称': [((w.wss(row[0], "comp_name")).Data)[0][0]], '行权收益率': [xingquanshouyi]
                                 , '绝对收益率': [jueduishouyi], '成交价格': [chengjiaoe], '成交量': [chengjiaoliang],
                              '全价': [shoupanquanjia], '行权日': [date]}),
                ignore_index=True)

def main():
    everything = pd.read_excel("bonds.xlsx", encoding='gbk')
    # print(bank.iloc[:,0:2])
    w.start()
    # print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # 获取当前时间
    shichang = pd.DataFrame(columns=('证券代码', '证券简称', '公司名称', '行权收益率', '绝对收益率', '成交价格', '成交量', '全价', '行权日'))
    find_product(everything, shichang)
    shichang.to_excel("市场跟踪.xlsx", index=False, header=True)
    #最终并不保存，只作为中间结果供2_2使用

main()
