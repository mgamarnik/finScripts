import pendulum
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import numpy as np
from perfCalc import perfCalc
import matplotlib.pyplot as plt

def printTick(tkr,tFrame,datInterval,days,key):
    #ID Ticker of interest and pull data
    dat = yf.Ticker(tkr)
    dInfo = dat.info #Ticker info
    df = dat.history(period = tFrame, interval = datInterval) #Ticker Dataframe

    #Dataframe of close prices
    closes = df['Close']

    #initializing long and exit arrays
    lArr = []
    lArrt = []
    eArr = []
    eArrt = []

    #List of times pulled from dataframe
    times = list(df.index)

    #Short SMA and Derivative--------------------------------------------------------------------------------------
    ssma50 = ta.sma(closes,length=50)
    # print(ssma50)
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
    xMaDiff = np.diff(xMa14) #RSI Moving Average Derivative
    xmL = list(xMaDiff) #List of RSI MA Derivative
    xmL = np.pad(xmL,(1,0)) #shifting rsi 14 gradient fwd 1 day

    #MACD------------------------------------------------------------------------------------------------------------
    xMacd = ta.macd(closes, fast=12, slow=26, signal=9, append=True) #MACD dataframe
    xMD = np.array(xMacd.MACD_12_26_9) #MACD Line as array
    xMDh = np.array(xMacd.MACDh_12_26_9) #MACD Histogram as array
    xMDs = np.array(xMacd.MACDs_12_26_9) #MACD Signal line as array

    #removing nans for math
    xMD = xMD[~np.isnan(xMD)]
    xMDh = xMDh[~np.isnan(xMDh)]
    xMDs = xMDs[~np.isnan(xMDs)]

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
    xMDh = np.pad(xMDh,(mismat,0))
    xMDs = np.pad(xMDs,(mismat,0))

    #Generating Buy/Sell Signals--------------------------------------------------------------------------------
    cInv = 0
    bs = []
    nSells = 0
    nBuys = 0
    for i in range(len(closes)-1):

        #Pulling data for current close
        ci = closes[i]
        xri = xrL[i]
        xmi = xmL[i]
        
        mdCOi = mdCO[i]
        mdCUi = mdCU[i]
        mdSi = xMDs[i]

        dssmai50 = dssma50[i]
        dssmai20 = dssma20[i]
        ssmai20 = ssma20[i]

        lmi = lMid[i]

        logicBuy = []
        logicSell = []

        if key == 'bbmd':
            logicBuy = (mdCOi == 1) & (dssmai20<0) & (mdSi<0) & (cInv <3) & (ci>lmi) & (ci<ssmai20)
            logicSell = (mdCUi == 1) & (mdSi>0) & (cInv > 0)
        elif key == 'rsimd':
            logicBuy = (xmi>0) & (xri<=32.5) & (dssmai50<0) & (cInv <3)
            logicSell = (mdCUi == 1 or xri > 70) & (mdSi>0) & (cInv > 0)
        else:
            print("invalid key")
            break

        if logicBuy:
    #         print(str(times[i])[0:10], xmi, xri, dssmai, cInv) #helpful in seeing when buys made
            #adding data to long array and buy/sell matrix
            lArr.append(closes[i])
            lArrt.append(times[i])
            bs.append([0,closes[i],str(times[i])[0:10]])
            cInv += 1
            nBuys += 1
        elif logicSell:
            #adding data to the exit array and buy/sell matrix
            eArr.append(closes[i])
            eArrt.append(times[i])
            bs.append([1,closes[i],str(times[i])[0:10]])
            cInv = 0
            nSells += 1
            
    # print(np.transpose(np.transpose(bs)))   
    ub = np.ones(len(times))*70
    lb = np.ones(len(times))*30

    sDate = len(times)-days
    #xma14, xr, times, xmd, xmds, xmdh,larrt, larr, earrt, earr
    #RSI PLOT-------------------------------------------------
    fig1 = plt.figure(1,figsize=(20, 10))
    ts = list(times)
    xmas = list(xMa14)
    xrs = list(xr)
    plt.plot(ts[sDate:-1], xmas[sDate:-1],'y', linewidth=2)
    plt.plot(ts[sDate:-1], xrs[sDate:-1],'m',linewidth=1)
    plt.legend(['RSI 14 SMA','RSI 14','Hist'])

    plt.plot(ts[sDate:-1], ub[sDate:-1],'--r',linewidth = 0.5)
    plt.plot(ts[sDate:-1], lb[sDate:-1],'--r',linewidth = 0.5)
    plt.title('rsi 14 ')
    plt.xlabel('Time')
    plt.ylabel('Close')
    plt.ylim(0, 100)
    plt.grid()
    plt.show()

    #MACD PLOT---------------------------------------------------
    fig2 = plt.figure(2,figsize=(20, 10))
    plt.plot(ts[sDate:-1], xMD[sDate:-1],'-b')
    plt.plot(ts[sDate:-1], xMDs[sDate:-1],'-r')
    plt.bar(ts[sDate:-1], xMDh[sDate:-1],color = 'maroon')
    plt.legend(['MACD','Signal','Hist'])
    plt.plot(ts[sDate:-1], np.zeros(len(ts[sDate:-1])),'-k')
    plt.grid()
#     plt.ylim(-12.5, 12.5)
    plt.show()
    
    
    lArrtCorr = lArrt[sDate:-1]
    lArrCorr = lArrt[sDate:-1]
    eArrtCorr = lArrt[sDate:-1]
    eArrCorr = lArrt[sDate:-1]
    #CLOSES PLOT with long and exit indicators----------------------------------------------------
    fig3 = plt.figure(3,figsize=(20, 10))
    plt.plot(ts[sDate:-1],closes[sDate:-1],'k', linewidth=1)
    plt.plot(lArrt[sDate:-1][sDate:-1],lArr[sDate:-1],'*g')
    plt.plot(eArrt[sDate:-1],eArr[sDate:-1],'*r')
    for k in range(len(lArr)):                                      
        plt.annotate('Buy 1 Share',xy =(lArrt[k],lArr[k]))
    for v in range(len(eArr)):                                      
        plt.annotate('Sell All Shares',xy =(eArrt[v],eArr[v]))
    plt.grid()
    plt.show()


    
    return