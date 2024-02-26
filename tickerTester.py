 #function with all the math
from scoreCalc import scoreCalc
# import pendulum
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import numpy as np
from perfCalc import perfCalc


def tickerTester(tkr,tFrame,key,pyd):

    #ID Ticker of interest and pull data
    dat = yf.Ticker(tkr)
    dInfo = dat.info #Ticker info
    # print(dInfo)
    df = dat.history(period = tFrame, interval = '1d') #Ticker Dataframe

    #Dataframe of close prices
    closes = df['Close']
    #List of times pulled from dataframe
    times = list(df.index)

    #Short SMA and Derivative--------------------------------------------------------------------------------------
    ssma50 = ta.sma(closes,length=50)
    dssma50 = np.diff(ssma50)
    ssma20 = ta.sma(closes,length=20)
    dssma20 = np.diff(ssma20)

    #Bollinger Band
    stdsma = 2*np.std(closes)
    devMid = 0.5*np.std(closes)
    uMid = ssma20+devMid
    lMid = ssma20-devMid

    #RSI 14----------------------------------------------------------------------------------------------------------
    xr = ta.rsi(closes, length = 14) #RSI Dataframe
    xrL = list(xr) #List of RSI Values
    xMa14 = ta.sma(xr, length = 14) #RSI Moving Average
    xMa14 = np.array(xMa14)
    xMaDiff = np.diff(xMa14) #RSI Moving Average Derivative
    # xMaDiff = xMa14[1:len(xMa14)]-xMa14[0:len(xMa14)-1] #RSI Moving Average Derivative
    xmL = list(xMaDiff) #List of RSI MA Derivative
    xmL = np.pad(xmL,(1,0)) #shifting rsi 14 gradient fwd 1 day

    #MACD------------------------------------------------------------------------------------------------------------
    xMacd = ta.macd(closes, fast=12, slow=26, signal=9, append=True) #MACD dataframe
    xMD = np.array(xMacd.MACD_12_26_9) #MACD Line as array
    xMDh = xMacd.MACDh_12_26_9 #MACD Histogram as array
    # xMDhDiff = ta.sma(xMDh,length=9)
    xMDhDiff = np.array(xMDh)
    xMDs = np.array(xMacd.MACDs_12_26_9) #MACD Signal line as array

    #removing nans for math
    xMD = xMD[~np.isnan(xMD)]
    xMDhDiff = xMDhDiff[~np.isnan(xMDh)]
    xMDs = xMDs[~np.isnan(xMDs)]
    xMDhDiff = np.diff(xMDhDiff)


    #cutting macd line to be same length as signal and hist
    xMD = xMD[(len(xMD)-len(xMDs)):len(xMD)] 
    mismat = len(times) - len(xMD) #recording data size mismatch

    #MACD Crossunder Signal line indicator
    mdCO = abs(np.diff(np.floor((xMD-xMDs)/(max(abs(xMD-xMDs))))))
    mdCU = abs(np.diff(np.ceil((xMD-xMDs)/(max(abs(xMD-xMDs))))))

    #Adding 0s to MACD arrays to be same length as time
    mdCU = np.pad(mdCU,(mismat,0))
    mdCO = np.pad(mdCO,(mismat,0))
    xMD = np.pad(xMD,(mismat,0))
    xMDhDiff = np.pad(xMDhDiff,(mismat,0))
    xMDs = np.pad(xMDs,(mismat,0))

    # print("MDCU Indicator")
    # print(mdCU)
    # print("\n")
    # print("MD Signal Line")
    # print(xMD)



    #Generating Buy/Sell Signals--------------------------------------------------------------------------------
    cInv = 0

    bs = []
    nSells = 0
    nBuys = 0
    openTol = 10
    dateOpenMD = 0
    dateOpenRSI = 0
    
    for i in range(len(closes)-1):

        #Pulling data for current close
        ci = closes[i]
        xri = xrL[i]
        xmi = xmL[i]
        
        mdCOi = mdCO[i]
        mdCUi = mdCU[i]
        mdSi = xMDs[i]
        mdi = xMD[i]
        mdHDi = xMDhDiff[i]

        dssmai50 = dssma50[i]
        dssmai20 = dssma20[i]
        ssmai20 = ssma20[i]

        lmi = lMid[i]

        logicBuy = []
        logicSell = []

        if key == 'bbmd':
            logicBuy = (mdCOi == 1) & (dssmai20<0) & (mdSi<0) & (cInv < pyd) & (ci>lmi) & (ci<ssmai20)
            logicSell = ((mdCUi == 1) & (mdSi>0) & (cInv > 0)) or ((xri >= 70) & (cInv > 0))
        elif key == 'rsimd': #original rsi based buy signals only
            logicBuy = (xmi>0) & (xri<32.5) & (dssmai50<0) & (cInv < pyd)
            logicSell = (mdCUi == 1 or xri > 70) & (mdSi>0) & (cInv > 0)
        elif key == 'rsimd2': #uses rsi and md histogram as buy indicator
            logicBuy = (xmi>0) & (xri<32.5) & (dssmai50<0) & (mdHDi>0) & (cInv < pyd)
            logicSell = (mdCUi == 1 or xri > 70) & (mdSi>0) & (cInv > 0)
        elif key == 'rsimd3':
            logicBuy = (mdi>mdSi) & (mdSi<0) & (mdi<0) & (xmi>0) & (xri<32.5) & (dssmai50<0) & (cInv < pyd)
            logicSell = (mdCUi == 1 or xri > 70) & (mdSi>0) & (cInv > 0)
        elif key == 'rsimd4': #uses rsi and md > signal as buy indicator
            
            if (mdi>mdSi) & (mdSi<0) & (mdi<0):
                dateOpenMD = openTol

            if (xmi>0) & (xri<32.5) & (dssmai50<0):
                dateOpenRSI = openTol

            if ((dateOpenMD + dateOpenRSI) > 0) & (cInv < pyd):
                logicBuy = True

            dateOpenRSI -= 1
            dateOpenMD -= 1
            logicSell = (mdCUi == 1 or xri > 70) & (mdSi>0) & (cInv > 0)
            # #           md>signal   signal<0    md<0    diffrsi14>0  rsi<32.5    diffsma50<0  pyramiding
        else:
            print("invalid key")
            break

        if logicBuy:
    #         print(str(times[i])[0:10], xmi, xri, dssmai, cInv) #helpful in seeing when buys made
            #adding data to long array and buy/sell matrix
            bs.append([0,closes[i],str(times[i])[0:10],i])
            cInv += 1
            nBuys += 1
        elif logicSell:
            #adding data to the exit array and buy/sell matrix
            bs.append([1,closes[i],str(times[i])[0:10],i])
            cInv = 0
            nSells += 1

    dOffset = 0
    lInd = -1

    if nSells>0:
        dOffset = len(closes)-bs[-1][3]-1 #number of days since last purchase   
    #OFFSET STUDY ONLY (need off boolean as input)

        # if off:
        #     bs2 = []
        #     cPrice = closes[-1]
        #     if bs[-1][0] == 0:
        #         # print(dOffset)
        #         for j in bs:
        #             idx = j[3]
        #             if j[0] == 0:
        #                 bs2.append([j[0],closes[idx+dOffset],str(times[idx+dOffset])[0:10],idx+dOffset]) #if current is less than original buy 
        #             else:
        #                 bs2.append([j[0],j[1],j[2],idx])

        #         bs = bs2

        #number of open buys
        lInd = -1
        while bs[lInd][0]==0:
            lInd -= 1

    
    mk = 0
    if 'marketCap' in list(dInfo):
        mk = dInfo['marketCap']

    fundData = [dInfo['industry'], dInfo['sector'], round(dInfo['marketCap']/10**9,3), dInfo['previousClose']]


    return bs, nSells, dOffset, abs(lInd+1), fundData, closes[-1] #buy/sell matrix, number of sell signals, days since last buy/sell, number of open buys, ticker fundamental data



