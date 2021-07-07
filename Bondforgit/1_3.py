import os
import numpy as np
import pandas as pd
import xlrd
from WindPy import w
import math

def merge_duizhang():
    duizhangdan = pd.DataFrame(pd.read_excel("对账单集合.xlsx"))
    date = duizhangdan.loc[0,"对账单合集"]
    #print(date)
    tag = 0
    file_dir = ".\\lists"  # file directory
    target = "对账单"
    all_csv_list = os.listdir(file_dir)  # get csv list
    latest=date
    for single_csv in all_csv_list:
        tag = 0
        if target in single_csv:
            filename = single_csv
            dataset = pd.DataFrame(pd.read_excel(file_dir + "\\" + filename))
            #print(dataset.loc[2,"Unnamed: 1"])
            if (int(dataset.loc[2,"Unnamed: 1"]) < date):
                continue
            if (int(dataset.loc[2,"Unnamed: 1"]) > latest):
                latest = int(dataset.loc[2,"Unnamed: 1"])
            for index,row in dataset.iterrows():
                if row[0]=="期初余额":
                    tag = index+1
            while dataset.loc[tag,"Unnamed: 1"]!="证券代码":
                if dataset.loc[tag,"Unnamed: 1"]=="证券买入" or dataset.loc[tag,"Unnamed: 1"] == "证券卖出":
                    tmp=[]
                    tmp.append(dataset.loc[tag,"资金对账单（人民币）"])
                    tmp.append(dataset.loc[tag,"Unnamed: 1"])
                    tmp.append(dataset.loc[tag,"Unnamed: 3"])
                    tmp.append(dataset.loc[tag,"Unnamed: 4"])
                    tmp.append(dataset.loc[tag,"Unnamed: 5"])
                    tmp.append(dataset.loc[tag,"Unnamed: 6"])
                    tmp.append(dataset.loc[tag,"Unnamed: 8"])
                    #dataframe拼接
                    b = pd.DataFrame(tmp).T
                    b.columns = duizhangdan.columns
                    duizhangdan=pd.concat([duizhangdan,b])
                    # dataframe拼接
                tag+=1
    duizhangdan.loc[0, "对账单合集"] = latest
    duizhangdan.to_excel("对账单集合.xlsx",index=False,header=True)
    return duizhangdan

#计算单支债券绝对收益
def bond_gain(bond,duizhangdan,code):
    sum_gain = 0
    sum_pay = 0
    hold_num = 0
    jiaquanchengben = 0
    buy_times = 0
    sum_payback = 0
    for index, row in duizhangdan.iterrows():
        if bond == row["Unnamed: 3"]:
            tradedate = "tradeDate=" + str(row["对账单合集"])
            if row["Unnamed: 1"] == "证券买入":
                buy_times += 1
                inf = (w.wss(code, "couponrate3,ptmyear,termifexercise", tradedate)).Data
                # print(inf)
                lilv = float(''.join([str(x) for x in inf[0]])) / 100
                rest_date = float(''.join([str(x) for x in inf[1]]))
                xingquan = float(''.join([str(x) for x in inf[2]]))
                #判断行权期限是不是空
                if xingquan != xingquan:
                    times = math.ceil(rest_date)
                else:
                    times = math.ceil(xingquan)
                payback = 100 * (1 + lilv * times)
                absgain_per = payback / float(abs(float(row["Unnamed: 6"])) / int(row["Unnamed: 4"])) -1
                absgain = absgain_per * abs(float(row["Unnamed: 6"]))
                sum_gain += absgain
                sum_pay += abs(float(row["Unnamed: 6"]))
                hold_num += int(row["Unnamed: 4"])
                sum_payback += payback
                if jiaquanchengben == 0:
                    jiaquanchengben = float(sum_pay / hold_num)
                else:
                    jiaquanchengben = (abs(float(row["Unnamed: 6"])) + jiaquanchengben * (
                                hold_num - int(row["Unnamed: 4"]))) / hold_num
            elif row["Unnamed: 1"] == "证券卖出":
                sum_gain -= ((sum_payback / buy_times - jiaquanchengben) * int(row["Unnamed: 4"]))
                hold_num -= int(row["Unnamed: 4"])
    return sum_gain

def main():
    product_gain = 0
    date = input("输入日期\n")
    chart = "估值表_" + date
    file_dir = ".\\lists"  # file directory
    all_csv_list = os.listdir(file_dir)  # get csv list
    for single_csv in all_csv_list:
        if chart in single_csv:
            filename = single_csv
            # 将所有债券名称存到bonds中
            # print(single_csv)
            dataset = pd.DataFrame(pd.read_excel(file_dir + "\\" + filename))
            shishouziben=0
            bonds = []
            wenxin=''
            for index, row in dataset.iterrows():
                # 找出债券名称
                if str(row[0])[-2:] == 'SH' or str(row[0])[-2:] == 'SZ' or str(row[0])[-2:] == 'IB' and str(row[0])[-9]!='6' and not (row[14]!=row[14]):
                    bonds.append(row[1])
                # 找出稳鑫表
                elif "OTC" in str(row[0]):
                    wenxin = row[1]
                elif str(row[0])=="实收资本":
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
            wenxinname = wenxin + '_' + '[' + date[0:4] + '-' + date[4:6] + '-' + date[6:8] + ']'
            #print(wenxinname)
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

            # 读取所有对账单
            duizhangdan = merge_duizhang()
            # print(duizhangdan)

            # 遍历债券
            w.start()
            #从wind提取所有债券名称和代码
            #everything = (w.wset("sectorconstituent","date=2021-06-07;sectorid=a101010801000000;field=wind_code,sec_name")).Data
            everything = pd.read_excel("bonds.xlsx", encoding='gbk')
            for bond in all_bonds:
                for index, row in everything.iterrows():
                    if row[1] == bond:
                        print(row)
                        code = row[0]
                        product_gain += bond_gain(bond, duizhangdan, code)
                        break
                #计算产品绝对收益
            print(product_gain)
            product_gainper = product_gain/shishouziben
            print(product_gainper)

main()
#提取所有交易所债券
#w.wset("sectorconstituent","date=2021-06-07;sectorid=1000022281000000")
#提取所有银行间债券
#w.wset("sectorconstituent","date=2021-06-07;sectorid=a101010801000000")
#股票绝对利益还没算！
#
#
#
