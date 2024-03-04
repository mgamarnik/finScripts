# import plotly.express as px 
from printTick import printTick
import matplotlib.pyplot as plt
import numpy as np
from tickerTester import tickerTester
import yfinance as yf
from procRes import procRes
import pandas as pd
import pandas_ta as ta


# key = 'bbmd'
key = 'rsimd'
tkr = 'jwn'
days = 365
datInterval = '1d'
pyd = 3
tFrame = 'max'
off = False

#ID Ticker of interest and pull data
dat = yf.Ticker(tkr)
dInfo = dat.info #Ticker info
# print(dInfo)
df = dat.history(period = tFrame, interval = '1d') #Ticker Dataframe

#Dataframe of close prices
closes = df['Close']
vol = df['Volume']
print(vol)

# #initializing long and exit arrays
# lArr = []
# lArrt = []
# eArr = []
# eArrt = []

# #List of times pulled from dataframe
# times = list(df.index)

# #Short SMA and Derivative--------------------------------------------------------------------------------------
# ssma50 = ta.sma(closes,length=50)
# dssma50 = np.diff(ssma50)
# ssma20 = ta.sma(closes,length=20)
# dssma20 = np.diff(ssma20)

# dssma50 = dssma50[~np.isnan(dssma50)]
# dssma20 = dssma20[~np.isnan(dssma20)]

# #Bollinger Band
# stdsma = 2*np.std(closes)
# devMid = 0.5*np.std(closes)
# uMid = ssma20+devMid
# lMid = ssma20-devMid

# #RSI 14----------------------------------------------------------------------------------------------------------
# xrL = ta.rsi(closes, length = 14) #RSI Dataframe
# xMa14 = ta.sma(xrL, length = 14) #RSI Moving Average
# # xMaDiff = np.diff(xMa14) #RSI Moving Average Derivative
# xMa14 = np.array(xMa14)
# xMaDiff = xMa14[1:len(xMa14)]-xMa14[0:len(xMa14)-1] #RSI Moving Average Derivative
# xmL = xMaDiff

# xMa14 = xMa14[~np.isnan(xMa14)]
# xrL = xrL[~np.isnan(xrL)]
# xmL = xmL[~np.isnan(xmL)]
# # print(xmL)



# #MACD------------------------------------------------------------------------------------------------------------
# xMacd = ta.macd(closes, fast=12, slow=26, signal=9, append=True) #MACD dataframe
# xMD = np.array(xMacd.MACD_12_26_9) #MACD Line as array
# xMDh = np.array(xMacd.MACDh_12_26_9) #MACD Histogram as array
# xMDs = np.array(xMacd.MACDs_12_26_9) #MACD Signal line as array

# #removing nans for math
# xMD = xMD[~np.isnan(xMD)]
# xMDh = xMDh[~np.isnan(xMDh)]
# xMDs = xMDs[~np.isnan(xMDs)]

# print(len(times)-len(dssma50))

# #cutting arrays to same length
# times = times[(len(times)-len(dssma50)):len(times)] 
# ssma20 = ssma20[(len(ssma20)-len(dssma50)):len(ssma20)] 
# dssma20 = dssma20[(len(dssma20)-len(dssma50)):len(dssma20)] 
# xMa14 = xMa14[(len(xMa14)-len(dssma50)):len(xMa14)] 
# xrL = xrL[(len(xrL)-len(dssma50)):len(xrL)] 
# xmL = xmL[(len(xmL)-len(dssma50)):len(xmL)]
# xMD = xMD[(len(xMD)-len(dssma50)):len(xMD)] 
# xMDh = xMDh[(len(xMDh)-len(dssma50)):len(xMDh)] 
# xMDs = xMDs[(len(xMDs)-len(dssma50)):len(xMDs)] 
# closes =  closes[(len(closes)-len(dssma50)):len(closes)] 

# mismat = len(times) - len(xMDs) #recording data size mismatch

# #cutting macd line to be same length as signal and hist

# # print("closes: ", len(closes))
# # print("xmL: ", len(xmL))
# # print("xrL: ", len(xrL))
# # print("xMD: ", len(xMD))
# # print("xMDh: ", len(xMDh))
# # print("xMDs: ", len(xMDs))
# # print("mismat: ", mismat)

# idx = 10914
# print(xmL[idx])
# print(xrL[idx])
# print(xMa14[idx])
# print(times[idx])

# #MACD Crossunder Signal line indicator
# mdCO = abs(np.diff(np.floor((xMD-xMDs)/(max(abs(xMD-xMDs))))))
# mdCU = abs(np.diff(np.ceil((xMD-xMDs)/(max(abs(xMD-xMDs))))))

# # #Adding 0s to MACD arrays to be same length as time
# # mdCU = np.pad(mdCU,(mismat,0))
# # mdCO = np.pad(mdCO,(mismat,0))
# # xMD = np.pad(xMD,(mismat,0))
# # xMDh = np.pad(xMDh,(mismat,0))
# # xMDs = np.pad(xMDs,(mismat,0))

# # print(xMD)
# # print("MDCU Indicator")
# # print(mdCU)
# # print("\n")
# # print("MD Signal Line")
# # print(xMD)



# #Generating Buy/Sell Signals--------------------------------------------------------------------------------
# cInv = 0

# bs = []
# nSells = 0
# nBuys = 0
# for i in range(len(closes)-1):

#     #Pulling data for current close
#     ci = closes[i]
#     xri = xrL[i]
#     xmi = xmL[i]
    
#     mdCOi = mdCO[i]
#     mdCUi = mdCU[i]
#     mdSi = xMDs[i]

#     dssmai50 = dssma50[i]
#     dssmai20 = dssma20[i]
#     ssmai20 = ssma20[i]

#     lmi = lMid[i]

#     logicBuy = []
#     logicSell = []

#     if key == 'bbmd':
#         logicBuy = (mdCOi == 1) & (dssmai20<0) & (mdSi<0) & (cInv < pyd) & (ci>lmi) & (ci<ssmai20)
#         logicSell = ((mdCUi == 1) & (mdSi>0) & (cInv > 0)) or ((xri >= 70) & (cInv > 0))
#     elif key == 'rsimd':
#         logicBuy = (xmi>0) & (xri<32.5) & (dssmai50<0) & (cInv < pyd)
#         logicSell = (mdCUi == 1 or xri > 70) & (mdSi>0) & (cInv > 0)
#     else:
#         print("invalid key")
#         break

#     if logicBuy:
# #         print(str(times[i])[0:10], xmi, xri, dssmai, cInv) #helpful in seeing when buys made
#         #adding data to long array and buy/sell matrix
#         lArr.append(closes[i])
#         lArrt.append(times[i])
#         bs.append([0,closes[i],str(times[i])[0:10],i])
#         cInv += 1
#         nBuys += 1
#     elif logicSell:
#         #adding data to the exit array and buy/sell matrix
#         eArr.append(closes[i])
#         eArrt.append(times[i])
#         bs.append([1,closes[i],str(times[i])[0:10],i])
#         cInv = 0
#         nSells += 1

# print(np.transpose(np.transpose(bs)))   


# # ub = np.ones(len(times))*70
# # lb = np.ones(len(times))*30

# # sDate = len(times)-days
# # #xma14, xr, times, xmd, xmds, xmdh,larrt, larr, earrt, earr
# # #RSI PLOT-------------------------------------------------
# # fig1 = plt.figure(1,figsize=(20, 10))
# # ts = list(times)
# # xmas = list(xMa14)
# # xrs = list(xr)
# # plt.plot(ts[sDate:-1], xmas[sDate:-1],'y', linewidth=2)
# # plt.plot(ts[sDate:-1], xrs[sDate:-1],'m',linewidth=1)
# # plt.legend(['RSI 14 SMA','RSI 14','Hist'])

# # plt.plot(ts[sDate:-1], ub[sDate:-1],'--r',linewidth = 0.5)
# # plt.plot(ts[sDate:-1], lb[sDate:-1],'--r',linewidth = 0.5)
# # plt.title('rsi 14 ')
# # plt.xlabel('Time')
# # plt.ylabel('Close')
# # plt.ylim(0, 100)
# # plt.grid()
# # plt.show()
# # # printTick(tkr,tFrame,datInterval,365,key)