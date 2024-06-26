# import plotly.express as px 
from printTick import printTick
# import matplotlib.pyplot as plt
import numpy as np
from tickerTester import tickerTester
import yfinance as yf
from procRes import procRes
import pandas as pd
from scoreCalc import scoreCalc
from perfCalcCash import perfCalc



# algo = 'bbmd'
# algo = 'rsimd4'
algo = 'rsimdvol'
# algo = 'rsimd2'
t = 'car'
pyd = 1
tFrame = 'Max'
off = False 


bs, nSells, dOff, nOpen, fundDat, lastClose, pAge = tickerTester(t,tFrame,algo,pyd) #calculate buy/sell signals and extract close price
# print(bs)
# print(np.transpose(np.transpose(bs)))
perfDat = perfCalc(bs,nSells)
# print(perfDat)
# print(perfDat[7])
score = scoreCalc(perfDat)
# # print(score)



outArr = []
outArr.append([t,perfDat[0],perfDat[1],perfDat[2], perfDat[6], dOff, nOpen, fundDat[0], fundDat[1], fundDat[2], lastClose, score[0],score[1],score[2]]) #collecting outputted data into array

pd.set_option('display.max_columns', None)  
pd.set_option('display.max_rows', None)  
pd.set_option('display.expand_frame_repr', False)
# print(outArr)
titles = ['Stock', '%prof', 'avgTrade%', 'nTrades','avgDays','openSeshs','numOpen','Industry','Sector', 'MarketCap','Price','realAvg','ntFact','Score']
dfOut = procRes(outArr,titles)
print(dfOut)

# print(bs)
# printTick(t,tFrame,'1d',365,algo)
# print(dat[4])