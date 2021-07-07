import os
import numpy as np
import pandas as pd
import xlrd
from WindPy import w
import math


chart = "估值表_"
file_dir = ".\\lists"  # file directory
all_csv_list = os.listdir(file_dir)  # get csv list
fengkong = pd.DataFrame(columns=('产品名称', '持仓债券', '估值贡献'))
for single_csv in all_csv_list:
    if chart in single_csv:
        filename = single_csv
        # 将所有债券名称存到bonds中
        # print(single_csv)
        tag1 = 0
        tag2 = 0
        while filename[tag1] != '_':
            tag1 += 1
        tag2 = tag1 + 1
        while filename[tag2] != '_':
            tag2 += 1
        proname = filename[tag1:tag2 + 1]
        dataset = pd.DataFrame(pd.read_excel(file_dir + "\\" + filename))
        shishouziben=0
        zichanjingzhi = 0
        for index, row in dataset.iterrows():
            if row[0] == "资产净值":
                zichanjingzhi = row[14]
                break
        for index, row in dataset.iterrows():
            if (str(row[0])[-2:] == 'SH' or str(row[0])[-2:] == 'SZ' or str(row[0])[-2:] == 'IB') and not (row[14]!=row[14]):
                gongxian=(row[14]/zichanjingzhi)*100
                fengkong = fengkong.append(pd.DataFrame({'产品名称': [proname], '持仓债券': [row[1]], '估值贡献': [gongxian]}),
                ignore_index=True)
print(fengkong)



