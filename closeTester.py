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
    pyd = 3
    tkrs = np.array(tkrs.Open[:]) #Extracting tickers into a separate array
    # #Initialize arrays 
    cRSIMD = [] #analyzed with closed trades

    print("Analyzing: ")
    for t in tkrs: #looping through each ticker and running the technical analysis
        print(t," ")
        bs, nSells, dOff, nOpen, fundDat, lastClose = tickerTester(t,'max','rsimd4',pyd) #calculate buy/sell signals and extract close prices
        if nOpen == 0: #if an open trade currently does NOT exist
            perfDat = perfCalc(bs,nSells)  
            if perfDat[0] != '0':  
                lastMove = perfDat[-2][-1]
                print(bs[-1])
                cRSIMD.append([t,round(lastMove[0][0],2),int(lastMove[1][0]),round(lastMove[2][0],2),round(lastMove[3][0],2)])

    pd.set_option('display.max_columns', None)  
    dfrsimd = pd.DataFrame(cRSIMD,columns = ['Stock', 'Price Move', 'pDiff', 'Buy Price','Sell Price'])

    # print("\nRSIMD Sell List: ----------------------------------------------------------------\n")
    # print(dfrsimd)
    return dfrsimd