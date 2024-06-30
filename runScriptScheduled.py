import os
import numpy as np
from tickerTester import tickerTester
import pandas as pd
from procRes import procRes
from perfCalc import perfCalc
from scoreCalc import scoreCalc
from finviz.screener import Screener
from datetime import date
import schedule
import time
from closeTesterScheduled import closeTester
from sendEmail import sendEmail

#Analysis Settings------------------------------------------------

def scheduledRunScript():
    #Algo Key
    # algo = 'bbmd'
    # algo = 'rsimd'
    # algo = 'rsimd2' #rsi<32.5, diffrsi14>0, diffsma50<0, diffmdHist>0 (better score, better backtest performance, more trades, less reliable signals)
    # algo = 'rsimd3' #rsi<32.5, diffrsi14>0, diffsma50<0, mdLine>signalLine, mdLine<0, signalLine<0 (worse everything but more reliable signals)
    algo = 'rsimdvol' 
    pyd = 1
    cap = 1


    # Screener Filters
    allFilt = ['cap_smallover','geo_usa','ta_rsi_os40']
    # allFilt = ['cap_largeover','geo_usa','ta_rsi_os40']
    # allFilt = ['cap_smallover','geo_usa','ta_rsi_os40']
    # allFilt = ['cap_largeover','geo_usa','ta_rsi_os30']
    # allFilt = ['cap_smallover', 'geo_usa','ta_highlow52w_a0to5h'] #USA, Small Over Marketcap, 0-5% above 52week low

    #Runscript----------------------------------------------------------

    # Pull Tickers
    today = date.today()
    tdyDT = today.strftime("%b_%d_%Y") 
    stock_list = Screener(filters=allFilt, table='Performance', order='Market Cap')  # Get the performance table and sort it by price ascending

    # Export the screener results to .csv
    # stock_list.to_csv("stock.csv")
    # print(stock_list)

    #Get all tickers into a list
    allTicks = []
    for stock in stock_list:
        # print(stock) # Print symbol and price
        allTicks.append(stock['Ticker'])

    allTicks = np.array(allTicks) #Extracting tickers into a separate array
    # print(len(allTicks))

    #Initialize arrays 
    openArr = [] #analyzed with trades still open
    outArr = []
    nSkipped = 0
    print("Analyzing %d stocks" % len(allTicks))
    for t in allTicks: #looping through each ticker and running the technical analysis
        print(t," ")
        try: 
            bs, nSells, dOff, nOpen, fundDat, lastClose, pAge = tickerTester(t,'max',algo,pyd) #calculate buy/sell signals and extract close prices
            if len(bs)!=0 and nSells!=0:
                perfDat = perfCalc(bs,nSells, cap)    
                score = scoreCalc(perfDat)
                activityFactor = round(perfDat[2]*perfDat[6]/pAge*100,2)
                earningPerc = round((perfDat[-1]-cap)/cap*100,2)
                if nOpen > 0: #
                    #               [t, %prof,    avgTrade,   ntrades,  avgOpenDays,dOff, nopen, industry,   sector,     marketCap,  price       earning percentage,  activityFactor, score]
                    openArr.append([t,perfDat[0],perfDat[1],perfDat[2], perfDat[6], dOff, nOpen, fundDat[0], fundDat[1], fundDat[2], round(lastClose,2), earningPerc, activityFactor,score[2]]) #collecting outputted data into array
                else:
                    #               [t, %prof,    avgTrade,   ntrades,  avgOpenDays,dOff, nopen, industry,   sector,     marketCap,  price     earning percentage,  activityFactor, score]
                    outArr.append([t,perfDat[0],perfDat[1],perfDat[2], perfDat[6], dOff, nOpen, fundDat[0], fundDat[1], fundDat[2], round(lastClose,2), earningPerc, activityFactor,score[2]]) #collecting outputted data into array    
        except:
            print("Skipped")
            nSkipped += 1
            pass

    pd.set_option('display.max_columns', None)  
    pd.set_option('display.max_rows', None)  
    pd.set_option('display.expand_frame_repr', False)

    titles = ['Stock', '%prof', 'avgTrade%', 'nTrades','avgDays','openSeshs','numOpen','Industry','Sector', 'MarketCap', 'Price', 'Earning%','ActFact','Score']
    if len(openArr) == 0:
        print("\n No Open Tickers: ----------------------------------------------------------------\n")
    else:
        dfOpen = procRes(openArr,titles)
        print("\n Open Tickers: ----------------------------------------------------------------\n")
        print(dfOpen)
        dfOpen.to_csv(('./outs/' + algo + '_' + tdyDT + '_' + allFilt[0] + '_' + allFilt[1] + '_' + allFilt[2] + '_OPEN.csv'))


    dfOut = procRes(outArr,titles)
    print("\n Rest of Tickers: ----------------------------------------------------------------\n")
    print(dfOut)
    dfOut.to_csv(('./outs/' + algo + '_' + tdyDT + '_' + allFilt[0] + '_' + allFilt[1] + '_' + allFilt[2] + '_REST.csv'))

    dfClose = closeTester()

    sendEmail(dfOpen,dfClose)


schedule.every().monday.at("07:00").do(scheduledRunScript)
schedule.every().tuesday.at("07:00").do(scheduledRunScript)
schedule.every().wednesday.at("07:00").do(scheduledRunScript)
schedule.every().thursday.at("07:00").do(scheduledRunScript)
schedule.every().friday.at("07:00").do(scheduledRunScript)
# schedule.every().sunday.at("17:36").do(scheduledRunScript)

while True:
    schedule.run_pending()
    print("Run pending: ")
    # Sleep for 30 mins
    time.sleep(1800)
# scheduledRunScript()