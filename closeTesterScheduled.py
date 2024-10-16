import numpy as np
from tickerTesterV2 import tickerTesterV2
import pandas as pd

#Close tester
def closeTester(algo, pyd, cap,tFrame,inter):
    # Pull Tickers
    tkrs = pd.read_csv("open.txt")
    # print(tkrs)
    rsimd = np.array(tkrs.Open[:]) #Extracting tickers into a separate array
    rsimd = rsimd[~pd.isnull(rsimd)]

    # #Initialize arrays 
    cRSIMD = [] #analyzed with closed trades
    cBBMD = []

    print("Analyzing: ")
    for t in rsimd: #looping through each ticker and running the technical analysis
        print(t," ")
        bs, nSells, dOff, nOpen, fundDat, lastClose, pAge, trades, perfDat = tickerTesterV2(t,tFrame,inter,algo,pyd, cap) #calculate buy/sell signals and extract close prices
        try:
            if nOpen == 0: #if an open trade currently does NOT exist
                # print(perfDat) 
                # print(bs[-1])
                sellDate = bs.loc[len(bs)-1,"Date"]
                lenT = len(trades)-1
                cRSIMD.append([t,sellDate,round(trades.loc[lenT,"NetChange"],2),round(trades.loc[lenT,"pDiff"]*100,2),round(trades.loc[lenT,"BuyPrice"],2),round(trades.loc[lenT,"SellPrice"],2)])
                # print(cRSIMD)
        except:
            print("Skipped\n")
            pass
    pd.set_option('display.max_columns', None)  
    dfrsimd = pd.DataFrame(cRSIMD,columns = ['Stock','Date', 'Price Move', 'pDiff', 'Buy Price','Sell Price'])
    print(dfrsimd)
    
    return dfrsimd
