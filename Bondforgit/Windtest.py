from WindPy import w
import matplotlib.pyplot as plot
import pandas as pd
import numpy as np

w.start()
w.isconnected()

code = w.wset("sectorconstituent","date=2021-04-22;sectorid=6072fea6eb5e4f19cce7b220.U")
leng = len(code.Data[1])
codes = ','.join(code.Data[1][0:leng])
res = w.wss(codes, "sec_name,sec_englishname","tradeDate=20210411;priceAdj=U;cycle=D")
print(res)