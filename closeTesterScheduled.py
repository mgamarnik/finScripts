import numpy as np
from tickerTester import tickerTester
import pandas as pd
from perfCalc import perfCalc
from scoreCalc import scoreCalc
from procRes import procRes

#Close tester
def closeTester():
    # Pull Tickers
    tkrs = pd.read_csv("open.txt")
    # print(tkrs)
    pyd = 3
    rsimd = np.array(tkrs.Open[:]) #Extracting tickers into a separate array
    rsimd = rsimd[~pd.isnull(rsimd)]

    # #Initialize arrays 
    cRSIMD = [] #analyzed with closed trades
    cBBMD = []

    print("Analyzing: ")
    for t in rsimd: #looping through each ticker and running the technical analysis
        print(t," ")
        bs, nSells, dOff, nOpen, fundDat, lastClose, pAge = tickerTester(t,'max','rsimdvol',pyd) #calculate buy/sell signals and extract close prices
        try:
            if nOpen == 0: #if an open trade currently does NOT exist
                perfDat = perfCalc(bs,nSells)   
                # print(perfDat) 
                lastMove = perfDat[-2][-1]
                # print(bs[-1])

                cRSIMD.append([t,round(lastMove[0][0],2),int(lastMove[1][0]),round(lastMove[2][0],2),round(lastMove[3][0],2)])
        except:
            pass
    pd.set_option('display.max_columns', None)  
    dfrsimd = pd.DataFrame(cRSIMD,columns = ['Stock', 'Price Move', 'pDiff', 'Buy Price','Sell Price'])
    print(dfrsimd)
    
    return dfrsimd
