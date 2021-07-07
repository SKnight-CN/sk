import os
import numpy as np
import pandas as pd
import xlrd
from WindPy import w
import math

chart = "估值表_"
file_dir = ".\\lists"  # file directory
all_csv_list = os.listdir(file_dir)  # get csv list
jizhongdu = pd.DataFrame(columns=('产品名称', '持仓发行人', '集中度比例'))
everything = pd.read_excel("bonds.xlsx", encoding='gbk')
for single_csv in all_csv_list:
    if chart in single_csv:
        zichanjingzhi = 0
        filename = single_csv
        # 将所有债券名称存到bonds中
        # print(single_csv)
        dataset = pd.DataFrame(pd.read_excel(file_dir + "\\" + filename))
        bonds=[]
        companys=[]
        codes=[]
        shizhi=[]
        company_jingzhi=[]
        for index, row in dataset.iterrows():
            # 找出债券、股票名称
            if (str(row[0])[-2:] == 'SH' or str(row[0])[-2:] == 'SZ' or str(row[0])[-2:] == 'IB') and not (row[14]!=row[14]):
                bond=row[1]
                bonds.append(row[1])
                shizhi.append(row[11])
                for index1, row1 in everything.iterrows():
                    if row1[1] == bond:
                        companys.append(((w.wss(bond, "comp_name")).Data)[0][0])
                        codes.append(row1[0])
            elif row[0] == "资产净值":
                zichanjingzhi = row[14]
        all_companys = sorted(set(companys), key=companys.index)
        i=0
        while i < len(all_companys):
            company_jingzhi.append(0)
            i+=1

        for index1, code in enumerate(codes):
            for index, company in enumerate(all_companys):
                if ((w.wss(code, "comp_name")).Data)[0][0] == company:
                    company_jingzhi[index]+=shizhi[index1]
                    break
        for index,num in enumerate(company_jingzhi):
            company_jingzhi[index] = num/zichanjingzhi
            jizhongdu = jizhongdu.append(pd.DataFrame({'产品名称': [filename], '持仓发行人': [all_companys[index]], '集中度比例': [num/zichanjingzhi]}),
                                       ignore_index=True)


