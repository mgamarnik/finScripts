 #function with all the math
from scoreCalc import scoreCalc
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
    vol = df['Volume']
    #List of times pulled from dataframe
    times = list(df.index)

    #Short SMA and Derivative--------------------------------------------------------------------------------------
    ssma50 = ta.sma(closes,length=50)
    dssma50 = np.diff(ssma50)
    ssma20 = ta.sma(closes,length=20)
    dssma20 = np.diff(ssma20)

    dssma50 = dssma50[~np.isnan(dssma50)]
    dssma20 = dssma20[~np.isnan(dssma20)]

    #Volume SMA and Derivative--------------------------------------------------------------------------------------
    volSma = ta.sma(vol,length = 15)
    volDiff = np.diff(volSma)
    volDiff = volDiff[~np.isnan(volDiff)]

    #Bollinger Band
    stdsma = 2*np.std(closes)
    devMid = 0.5*np.std(closes)
    uMid = ssma20+devMid
    lMid = ssma20-devMid

    #RSI 14----------------------------------------------------------------------------------------------------------
    xrL = ta.rsi(closes, length = 14) #RSI Dataframe
    xMa14 = ta.sma(xrL, length = 14) #RSI Moving Average
    # xMaDiff = np.diff(xMa14) #RSI Moving Average Derivative
    xMa14 = np.array(xMa14)
    xMaDiff = xMa14[1:len(xMa14)]-xMa14[0:len(xMa14)-1] #RSI Moving Average Derivative
    xmL = xMaDiff

    xMa14 = xMa14[~np.isnan(xMa14)]
    xrL = xrL[~np.isnan(xrL)]
    xmL = xmL[~np.isnan(xmL)]
    # print(xmL)



    #MACD------------------------------------------------------------------------------------------------------------
    xMacd = ta.macd(closes, fast=12, slow=26, signal=9, append=True) #MACD dataframe
    xMD = np.array(xMacd.MACD_12_26_9) #MACD Line as array
    xMDh = np.array(xMacd.MACDh_12_26_9) #MACD Histogram as array
    xMDs = np.array(xMacd.MACDs_12_26_9) #MACD Signal line as array

    #removing nans for math
    xMD = xMD[~np.isnan(xMD)]
    xMDh = xMDh[~np.isnan(xMDh)]
    xMDs = xMDs[~np.isnan(xMDs)]

    # print(len(times)-len(dssma50))

    #cutting arrays to same length
    times = times[(len(times)-len(dssma50)):len(times)] 
    ssma20 = ssma20[(len(ssma20)-len(dssma50)):len(ssma20)] 
    dssma20 = dssma20[(len(dssma20)-len(dssma50)):len(dssma20)] 
    volDiff = volDiff[(len(volDiff)-len(dssma50)):len(volDiff)]
    xMa14 = xMa14[(len(xMa14)-len(dssma50)):len(xMa14)] 
    xrL = xrL[(len(xrL)-len(dssma50)):len(xrL)] 
    xmL = xmL[(len(xmL)-len(dssma50)):len(xmL)]
    xMD = xMD[(len(xMD)-len(dssma50)):len(xMD)] 
    xMDh = xMDh[(len(xMDh)-len(dssma50)):len(xMDh)] 
    xMDs = xMDs[(len(xMDs)-len(dssma50)):len(xMDs)] 
    closes =  closes[(len(closes)-len(dssma50)):len(closes)] 

    # mismat = len(times) - len(xMDs) #recording data size mismatch

    #MACD Crossunder Signal line indicator
    mdCO = abs(np.diff(np.floor((xMD-xMDs)/(max(abs(xMD-xMDs))))))
    mdCU = abs(np.diff(np.ceil((xMD-xMDs)/(max(abs(xMD-xMDs))))))

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
    dateOpenVol = 0
    
    for i in range(len(closes)-1):

        #Pulling data for current close
        ci = closes[i]
        xri = xrL[i]
        xmi = xmL[i]
        vi = volDiff[i]
        
        mdCOi = mdCO[i]
        mdCUi = mdCU[i]
        mdSi = xMDs[i]
        mdi = xMD[i]
        # mdHDi = xMDhDiff[i]

        dssmai50 = dssma50[i]
        dssmai20 = dssma20[i]
        ssmai20 = ssma20[i]

        lmi = lMid[i]

        logicBuy = []
        logicSell = []


        if key == 'rsimd4': #uses rsi and md > signal as buy indicator
            
            if (mdi>mdSi) & (mdSi<0) & (mdi<0):
                dateOpenMD = openTol

            if (xmi>0) & (xri<32.5) & (dssmai50<0):
                dateOpenRSI = openTol

            if ((dateOpenMD + dateOpenRSI) > 0) & (cInv < pyd):
                logicBuy = True

            dateOpenRSI -= 1
            dateOpenMD -= 1
            dateOpenVol -= 1
            logicSell = (mdCUi == 1 or xri > 70) & (mdSi>0) & (cInv > 0)
            #           md>signal   signal<0    md<0    diffrsi14>0  rsi<32.5    diffsma50<0  pyramiding
        elif key == 'rsimdvol': 
            if (mdi>mdSi) & (mdSi<0) & (mdi<0):
                dateOpenMD = openTol

            if (xmi>0) & (xri<32.5) & (dssmai50<0):
                dateOpenRSI = openTol

            if (vi>0):
                dateOpenVol = openTol

            if ((dateOpenMD + dateOpenRSI + dateOpenVol) > 20) & (cInv < pyd):
                logicBuy = True

            dateOpenRSI -= 1
            dateOpenMD -= 1
            dateOpenVol -= 1
            logicSell = (((mdCUi == 1) & (mdSi>0)) or (xri >= 67.5))  & (cInv > 0)
            #           md>signal   signal<0    md<0    diffrsi14>0  rsi<32.5    diffsma50<0  pyramiding
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

    fundData = [dInfo['industry'], dInfo['sector'], round(dInfo['marketCap']/10**9,3), dInfo['previousClose'], len(closes)]
    

    return bs, nSells, dOffset, abs(lInd+1), fundData, closes[-1], len(closes) #buy/sell matrix, number of sell signals, days since last buy/sell, number of open buys, ticker fundamental data



