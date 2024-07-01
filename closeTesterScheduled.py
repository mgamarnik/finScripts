import numpy as np
from tickerTesterV2 import tickerTesterV2
import pandas as pd

#Close tester
def closeTester(algo, pyd, cap):
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
        bs, nSells, dOff, nOpen, fundDat, lastClose, pAge, trades, perfDat = tickerTesterV2(t,'max',algo,pyd, cap) #calculate buy/sell signals and extract close prices
        try:
            if nOpen == 0: #if an open trade currently does NOT exist
                # print(perfDat) 
                # print(bs[-1])
                sellDate = bs["Date"][-1]
                cRSIMD.append([t,sellDate,round(trades["NetChange"][-1],2),int(trades["pDiff"][-1]),round(trades["BuyPrice"][-1],2),round(trades["SellPrice"][-1],2)])
                print(cRSIMD)
        except:
            print("Skipped\n")
            pass
    pd.set_option('display.max_columns', None)  
    dfrsimd = pd.DataFrame(cRSIMD,columns = ['Stock','Date', 'Price Move', 'pDiff', 'Buy Price','Sell Price'])
    print(dfrsimd)
    
    return dfrsimd
