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
w.start()
products = pd.read_csv("products.csv")
cuopei = pd.DataFrame(columns=('产品名称', '持仓债券', '期限错配比例'))
for single_csv in all_csv_list:
    if chart in single_csv:
        filename = single_csv
        # 将所有债券名称存到bonds中
        # print(single_csv)
        dataset = pd.DataFrame(pd.read_excel(file_dir + "\\" + filename))
        bonds = []
        codes = []
        shizhi = []

        kaifangri = ''
        jingzhi = 0
        #从表明提取产品明
        tag1=0
        tag2=0
        while filename[tag1]!='_':
            tag1+=1
        tag2=tag1+1
        while filename[tag2]!='_':
            tag2+=1
        proname = filename[tag1:tag2+1]
        #
        #找出产品开放日
        for row in products:
            if proname == row[0]:
                kaifangri = row[4]
                break
        for index, row in dataset.iterrows():
            # 找出债券名称
            if str(row[0])[-2:] == 'SH' or str(row[0])[-2:] == 'SZ' or str(row[0])[-2:] == 'IB' and str(row[0])[
                -9] != '6' and not (row[14] != row[14]):
                bonds.append(row[1])
                code = row[0][-9:]
                code = list(code)
                code[-3] = '.'
                code = ''.join(code)
                codes.append(code)
                shizhi.append(row[11])
            elif str(row[0])=="资产净值":
                jingzhi = row[11]
        for index,bond in enumerate(bonds):
            da = "date=" + str(int(time.strftime("%Y%m%d", time.localtime()))) +";type=All"
            date = list(((w.wss(codes[index], "nxoptiondate",da)).Data)[0])
            if date[0]!=None:
                date = list(date[0])
                print(type(date))
                print(len(date))
                print(date)
                date[4]=''
                date[7]=''
                date = ''.join(date)
                print(date)
                if date > kaifangri:
                    cuopei = cuopei.append(
                        pd.DataFrame({'产品名称': [proname], '持仓债券': [bond], '期限错配比例': [shizhi[index]/jingzhi]}),
                        ignore_index=True)



