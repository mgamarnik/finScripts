 #function with all the math
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import numpy as np
from diffPlus import diffPlus
import math
import warnings

def tickerTesterV2(tkr,tFrame,key,pyd,cap):
    warnings.filterwarnings("ignore")

    #ID Ticker of interest and pull data
    dat = yf.Ticker(tkr)
    dInfo = dat.info #Ticker info
    # print(dInfo)
    df = dat.history(period = tFrame, interval = '1d') #Ticker Dataframe

    #Dataframe of close prices
    closes = df['Close']
    vol = df['Volume']
    #List of times pulled from dataframe
    times = df.index

    #Short SMA and Derivative--------------------------------------------------------------------------------------
    sma200 = ta.sma(closes,length=200)
    sma50 = ta.sma(closes,length=50)
    sma20 = ta.sma(closes,length=20)
    sma30 = ta.sma(closes,length=30)

    df['MA200'] = sma200
    df['dMA200'] = diffPlus(sma200,1)
    df['MA50'] = sma50
    df['dMA50'] = diffPlus(sma50,5)
    df['dMA50roc50'] = diffPlus(sma50,50)
    df['MA20'] = sma20
    df['dMA20'] = diffPlus(sma20,1)
    df['MA30'] = sma30 
    df['dMA30'] = diffPlus(sma30,1)
    
    #Short EMA and Derivative--------------------------------------------------------------------------------------
    ema200 = ta.ema(closes,length=200)
    ema50 = ta.ema(closes,length=50)
    ema20 = ta.ema(closes,length=20)
    ema30 = ta.ema(closes,length=30)

    df['eMA200'] = ema200
    df['deMA200'] = diffPlus(ema200,20)
    df['eMA50'] = ema50
    df['deMA50'] = diffPlus(ema50,1)
    df['eMA20'] = ema20
    df['deMA20'] = diffPlus(ema20,1)
    df['eMA30'] = ema30 
    df['deMA30'] = diffPlus(ema30,1)

    #Volume SMA and Derivative--------------------------------------------------------------------------------------

    # volDiff = pd.DataFrame.diff(vol)
    # dVolSma = ta.sma(volDiff,length = 30)
    dVolSma = ta.ema(df['Volume'],length = 50)
    dVolSma = diffPlus(dVolSma,50)
    # df['dVol'] = volDiff
    df['dVol_MA50'] = dVolSma


    #RSI 14----------------------------------------------------------------------------------------------------------
    rsi14 = ta.rsi(closes, length = 14)
    df['rsi14'] = rsi14 #RSI Dataframe
    rsi14_MA14 = ta.sma(rsi14, length = 14) #RSI Moving Average
    df['rsi14_dMA14'] = diffPlus(rsi14_MA14,1)

    #KST------------------------------------------------------------------------------------------------------------
    kst = ta.kst(closes)
    df['kst'] = kst['KST_10_15_20_30_10_10_10_15']
    df['kstSig'] = kst['KSTs_9']


    #MACD------------------------------------------------------------------------------------------------------------
    xMacd = ta.macd(closes, fast=12, slow=26, signal=9, append=True) #MACD dataframe
    df['macdLine'] = xMacd.MACD_12_26_9
    df['macdHist'] = xMacd.MACDh_12_26_9
    df['macdSignal'] = xMacd.MACDs_12_26_9

    mdCO = np.floor((df['macdLine'].subtract(df['macdSignal']))/(df['macdLine'].subtract(df['macdSignal']).abs().max())).diff().abs()
    mdCU = np.ceil((df['macdLine'].subtract(df['macdSignal']))/(df['macdLine'].subtract(df['macdSignal']).abs().max())).diff().abs()
 
    df['mdCO'] = mdCO
    df['mdCU'] = mdCU
    # print(mdCU)

    kstCO = np.floor((df['kst'].subtract(df['kstSig']))/(df['kst'].subtract(df['kst']).abs().max())).diff().abs()
    kstCU = np.ceil((df['kst'].subtract(df['kstSig']))/(df['kst'].subtract(df['kst']).abs().max())).diff().abs()
 
    df['kstCO'] = mdCO
    df['kstCU'] = mdCU

    pd.set_option('display.max_columns', None)  
    pd.set_option('display.max_rows', None)  
    pd.set_option('display.expand_frame_repr', False)

    # print(df)

    # Generating Buy/Sell Signals--------------------------------------------------------------------------------
    cInv = 0

    bs = pd.DataFrame({"Signal":[],"Price":[],"Date":[],"Index":[]})
    trades = pd.DataFrame({"NetChange":[],"pDiff":[],"BuyPrice":[],"SellPrice":[],"nDays":[]})
    nSells = 0
    nBuys = 0
    openTol = 1
    dateOpenMD = 0
    dateOpenRSI = 0
    dateOpenVol = 0
    dateCloseMD = 0
    dateCloseRSI = 0
    dateCloseVol = 0
    jBuy = 0
    j = 0
    holdCrit = 0
    posChange = 0
    bull = False
    nCap = cap


    for i in df.index:

        #Pulling data for current close
        xri = df.loc[i,'rsi14']
        xmi = df.loc[i,'rsi14_dMA14']
        vdi = df.loc[i,'dVol_MA50']
        dsma30i = df.loc[i,'dMA30']
        sma50i = df.loc[i,'MA50']
        dMA50roc50i = df.loc[i,'dMA50roc50']
        sma200i = df.loc[i,'MA200']
        dsma200i = df.loc[i,'dMA200']
        ema200i = df.loc[i,'eMA200']
        dema200i = df.loc[i,'deMA200']


        # dema
        
        mdCOi = df.loc[i,'mdCO']
        mdCUi = df.loc[i,'mdCU']
        mdSi = df.loc[i,'macdSignal']
        mdi = df.loc[i,'macdLine']
        # mdHDi = xMDhDiff[i]
        kstSigi = df.loc[i,'kstSig']
        kstCOi = df.loc[i,'kstCO']
        kstCUi = df.loc[i,'kstCU']

        dsma50i = df.loc[i,'dMA50']
        closei = df.loc[i,'Close']

        logicBuy = []
        logicSell = []


        if key == 'rsimdvol': 

# OPEN CRITERIA-------------------------------------------------------------
            if (kstCOi == 1) & (kstSigi<0) & (dsma50i<0):
                dateOpenMD = openTol
            else:
                dateOpenMD = 0

            if (xmi>0) & (xri<32.5) & (dsma50i<0):
                dateOpenRSI = openTol
            else: 
                dateOpenRSI = 0

            if (vdi>0 and dsma50i<0):
                dateOpenVol = openTol
            else:
                dateOpenVol = 0

# OPEN LOGIC------------------------------------------------------------------
            if ((dateOpenMD + dateOpenRSI + dateOpenVol) >= 2) & (cInv < pyd):                
                logicBuy = True
                jBuy = j

# CURRENT POSITION CHANGE CALC--------------------------------------------------
            buyPrice = 0
            if cInv>0:
                buyPrice = bs.loc[len(bs)-1,"Price"]
                posChange = closei/buyPrice-1 #had this swapped, limited to 15% gain
            # print(posChange)
#SELL CRITERIA-----------------------------------------------------------------
            if ((kstCUi == 1) & (kstSigi>0) & (dsma50i>0)):
                dateCloseMD = 1
            else:
                dateCloseMD = 0

            if ((xri>70) & (xmi<0) & (dsma50i>0)):
                dateCloseRSI = 1
            else:
                dateCloseRSI = 0

            if ((vdi < 0) & (dsma50i>0)):
                dateCloseVol = 1
            else:
                dateCloseVol = 0


#EXTENDED HOLD CONDITION LOGIC-------------------------------------------------------
            if (closei>sma50i) & (sma50i>sma200i) & (cInv>0):
                logicSell = False
                holdCrit = 1
           
            if (closei<sma50i) & (holdCrit == 1) & (cInv>0):
                logicSell = True

#NOMINAL SELL LOGIC------------------------------------------------------------
            # if (((dateCloseMD + dateCloseRSI + dateCloseVol)>=2) or (posChange<=-0.15)) & (cInv > 0) & (holdCrit == 0):
            if (((dateCloseMD + dateCloseRSI + dateCloseVol)>=2) or ((j-jBuy)>60 and posChange<0) or (posChange<=-0.15)) & (cInv > 0) & (holdCrit == 0):
                logicSell = True
        elif key == 'avgsOnly':
            
            pPosB = closei>sma50i
            s50TrB = dsma50i>0
            # s50Pos = sma50i>eMA200i
            e200TrB = dema200i>0

            logicBuy = pPosB & s50TrB & e200TrB & (holdCrit == 0)
            if logicBuy: holdCrit = 1

            pPosS = closei<sma50i
            s50TrS = dsma50i<0

            logicSell = pPosS & s50TrS & (holdCrit == 1)
            if logicSell: holdCrit == 0

        elif key == 'smavol':
            
            buyPos = vdi>0 and dMA50roc50i<0
            logicBuy = buyPos & (cInv < pyd)            

            sellPos = vdi<0 and dMA50roc50i>0
            logicSell = sellPos & (cInv>0)            


        else:
            print("invalid key")
            break

        if dsma200i > 0: bull = True
        else: bull = False

        if logicBuy:
            #adding data to long array and buy/sell matrix
            bs = bs._append({"Signal":0,"Price":closei,"Date":i,"Index":j,"mdO":dateOpenMD,"rsiO":dateOpenRSI,"volO": dateOpenVol,"Bull?":bull},ignore_index=True)
            cInv += 1
            nBuys += 1
        elif logicSell:
            pDiff = (closei/bs.loc[len(bs)-1,"Price"])-1
            nDays = j-bs.loc[len(bs)-1,"Index"]
            #adding data to trades dataframe (ONLY WORKS WITH PYD=1 AT THE MOMENT)
            trades = trades._append({"NetChange":(closei-bs.loc[len(bs)-1,"Price"]),"pDiff":pDiff,"BuyPrice":bs.loc[len(bs)-1,"Price"],"SellPrice":closei,"nDays":nDays},ignore_index=True)
            #adding sell signal to bs dataframe
            bs = bs._append({"Signal":1,"Price":closei,"Date":i,"Index":j,"mdC":dateCloseMD,"rsiC":dateCloseRSI,"volC":dateCloseVol,"posChange":posChange,"holdD":(j-jBuy),"extHold":holdCrit,"Bull?":bull},ignore_index=True)
            nCap += nCap*pDiff
            cInv = 0
            nSells += 1
            jBuy = 0
            holdCrit = 0            

        
        j += 1

    if len(trades)>0:
        #Performance Stats
        avgTrade = round(trades['pDiff'].mean(),2)*100
        # avgTrade = round(np.mean(np.array(perf)[:,1]),2)
        pProf = round(len(trades[trades['pDiff']>0])/len(trades),2)*100
        avgDays = round(trades['nDays'].mean(),0)  
        earn = nCap-cap
        earnP = earn/cap*100
        perfDat = [pProf,avgTrade,len(trades),avgDays,earn, earnP]
    else:
        perfDat = [0,0,0,0,0,0]


    dOffset = 0
    lInd = -1
    # print(bs)
    if nSells>0:
        dOffset = len(df.index)-bs.loc[len(bs)-1,"Index"]-1 #number of days since last purchase  
        # print(bs.loc[len(bs["Index"])-1,"Index"])
        lInd = -1
        while int(bs.loc[len(bs)+lInd,["Signal"]].iloc[0])==0:
            lInd -= 1

    
    mk = 0
    fundData = []
    if 'marketCap' in list(dInfo):
        mk = dInfo['marketCap']
        fundData = [dInfo['industry'], dInfo['sector'], round(dInfo['marketCap']/10**9,3), dInfo['previousClose']]
    
     #buy/sell matrix, number of sell signals, days since last buy/sell, number of open buys, ticker fundamental data, last close price, number of days analyzed, trades df, performance arr
    return bs,                  nSells,          dOffset,                     abs(lInd+1),      fundData,               closes[-1],         len(closes),           trades,   perfDat


