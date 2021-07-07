import os
import numpy as np
import pandas as pd
import xlrd
from WindPy import w
import math
import time

chart = "估值表_"
file_dir = ".\\lists"  # file directory
all_csv_list = os.listdir(file_dir)  # get csv list
alert = pd.DataFrame(columns=('债券简称', '行权日', '产品名称'))
for single_csv in all_csv_list:
    if chart in single_csv:
        filename = single_csv
        # 将所有债券名称存到bonds中
        # print(single_csv)
        dataset = pd.DataFrame(pd.read_excel(file_dir + "\\" + filename))
        shishouziben = 0
        bonds = []
        wenxin = ''
        for index, row in dataset.iterrows():
            # 找出债券名称
            if str(row[0])[-2:] == 'SH' or str(row[0])[-2:] == 'SZ' or str(row[0])[-2:] == 'IB' and str(row[0])[
                -9] != '6' and not (row[14] != row[14]):
                bonds.append(row[1])
            # 找出稳鑫表
            elif "OTC" in str(row[0]):
                wenxin = row[1]
            elif str(row[0]) == "实收资本":
                shishouziben = float(row[6])
        # print(bonds)
        # 得到稳鑫表名
        temp = list(wenxin)
        temp.pop(-1)
        temp.pop(-3)
        temp.pop(-3)
        temp.pop(-11)
        temp.pop(-11)
        temp.pop(-11)
        temp.pop(-11)
        wenxin = ''.join(temp)
        for single_csv1 in all_csv_list:
            if wenxin in single_csv1:
                filename = single_csv1
                break

        # 读取温馨表
        dataset = pd.DataFrame(pd.read_excel(file_dir + "\\" + filename))
        for index, row in dataset.iterrows():
            # 找出债券名称
            if len(str(row[0])) == 14:
                # print(row)
                if (row[1][0] >= '0' and row[1][0] <= '9'):
                    bonds.append(row[1])
        # 去除重复债券,all_bonds为债券名字集合
        all_bonds = sorted(set(bonds), key=bonds.index)
        print(bonds)
        print(all_bonds)

        w.start()
        # 从wind提取所有债券名称和代码
        # everything = (w.wset("sectorconstituent","date=2021-06-07;sectorid=a101010801000000;field=wind_code,sec_name")).Data
        everything = pd.read_csv("bonds.csv", encoding='gbk')
        # 从表明提取产品明
        tag1 = 0
        tag2 = 0
        while filename[tag1] != '_':
            tag1 += 1
        tag2 = tag1 + 1
        while filename[tag2] != '_':
            tag2 += 1
        proname = filename[tag1+1:tag2]
        #
        for bond in all_bonds:
            for index, row in everything.iterrows():
                if row[1] == bond:
                    code = row[0]
                    da = str(int(time.strftime("%Y%m%d", time.localtime())))
                    date = "date=" + da + ";type=All"
                    xingquan = list(((w.wss(code, "nxoptiondate", date)).Data)[0])
                    if xingquan[0] != None:
                        xingquan = list(xingquan[0])
                        xingquan[4] = ''
                        xingquan[7] = ''
                        xingquan = ''.join(xingquan)
                        if (xingquan[0:4]==da[0:4]):
                            if (int(xingquan[4:6])-int(da[4:6])<=2):
                                alert = alert.append(pd.DataFrame({'债券简称': [bond], '行权日': [xingquan], '产品名称': [proname]}),
                ignore_index=True)
