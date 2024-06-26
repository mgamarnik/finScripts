import numpy as np
from tickerTester import tickerTester
import pandas as pd
from perfCalc import perfCalc
from scoreCalc import scoreCalc
from procRes import procRes

#Close tester

# Pull Tickers
tkrs = pd.read_excel("../open.xlsx")
# print(tkrs)
pyd = 3
rsimd = np.array(tkrs.RSIMD[:]) #Extracting tickers into a separate array
rsimd = rsimd[~pd.isnull(rsimd)]

bbmd = np.array(tkrs.BBMD[:])
bbmd = bbmd[~pd.isnull(bbmd)]


# #Initialize arrays 
cRSIMD = [] #analyzed with closed trades
cBBMD = []

print("Analyzing: ")
for t in rsimd: #looping through each ticker and running the technical analysis
    print(t," ")
    bs, nSells, dOff, nOpen, fundDat = tickerTester(t,'max','rsimd',pyd) #calculate buy/sell signals and extract close prices
    if nOpen == 0: #if an open trade currently does NOT exist
        perfDat = perfCalc(bs,nSells)    
        lastMove = perfDat[-2][-1]
        print(bs[-1])

        cRSIMD.append([t,round(lastMove[0][0],2),int(lastMove[1][0]),round(lastMove[2][0],2),round(lastMove[3][0],2)])

print("Analyzing: ")
for t in bbmd: #looping through each ticker and running the technical analysis
    print(t," ")
    bs, nSells, dOff, nOpen, fundDat = tickerTester(t,'max','bbmd',pyd) #calculate buy/sell signals and extract close prices
    if nOpen == 0: #if an open trade currently does NOT exist
        perfDat = perfCalc(bs,nSells)    
        lastMove = perfDat[-2][-1]
        cBBMD.append([t,round(lastMove[0][0],2),int(lastMove[1][0]),round(lastMove[2][0],2),round(lastMove[3][0],2)]) #collecting outputted data into array


pd.set_option('display.max_columns', None)  
dfrsimd = pd.DataFrame(cRSIMD,columns = ['Stock', 'Price Move', 'pDiff', 'Buy Price','Sell Price'])
dfbbmd = pd.DataFrame(cBBMD,columns = ['Stock', 'Price Move', 'pDiff', 'Buy Price','Sell Price'])

print("\nRSIMD Sell List: ----------------------------------------------------------------\n")
print(dfrsimd)

print("\nBBMD Sell List: -----------------------------------------------------------------\n")
print(dfbbmd)
