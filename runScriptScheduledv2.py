import os
import numpy as np
from tickerTesterV2 import tickerTesterV2
import pandas as pd
from finviz.screener import Screener
from datetime import date
from closeTesterScheduled import closeTester
from sendEmail import sendEmail
import schedule
import time

#Analysis Settings------------------------------------------------

def scheduledRunScript():
    #Algo Key
    # algo = 'bbmd'
    # algo = 'rsimd'
    # algo = 'rsimd2' #rsi<32.5, diffrsi14>0, diffsma50<0, diffmdHist>0 (better score, better backtest performance, more trades, less reliable signals)
    # algo = 'rsimd3' #rsi<32.5, diffrsi14>0, diffsma50<0, mdLine>signalLine, mdLine<0, signalLine<0 (worse everything but more reliable signals)
    


    # algo = 'rsimdvol' 
    algo = 'smavol'
    pyd = 1
    closeCap = 1
    inter = '1d'
    tFrame = 'max'
    dfClose = closeTester(algo, pyd, closeCap,tFrame,inter)


    # Screener Filters
    # allFilt = ['cap_largeover','geo_usa','ta_rsi_os40']
    allFilt = ['cap_largeover','geo_usa']
    # allFilt = ['cap_midover', 'geo_usa','ta_highlow52w_a0to10h'] #USA, Small Over Marketcap, 0-10% above 52week low
    # allFilt = ['cap_smallover', 'geo_usa','ta_highlow52w_a0to5h'] #USA, Small Over Marketcap, 0-5% above 52week low
    # allFilt = ['ind_aerospacedefense','geo_usa']
    # allFilt = ['cap_smallover','geo_usa','sec_consumerdefensive']

    #Runscript----------------------------------------------------------

    # Pull Tickers
    today = date.today()
    tdyDT = today.strftime("%b_%d_%Y") 
    # stock_list = None
    stock_list = Screener(filters=allFilt, table='Performance', order='Market Cap')  # Get the performance table and sort it by price ascending

    # Export the screener results to .csv
    # stock_list.to_csv("stock.csv")
    # print(len(stock_list))

    #Get all tickers into a list
    allTicks = []
    for stock in stock_list:
        # print(stock) # Print symbol and price
        allTicks.append(stock['Ticker'])

    allTicks = np.array(allTicks) #Extracting tickers into a separate array
    # print(len(allTicks))

    #Initialize arrays 
    newArr = pd.DataFrame({'Stock':[], 'pprof':[], 'avgTradeP':[], 'nTrades':[],'avgDays':[],'openSeshs':[],'numOpen':[],'Industry':[],'Sector':[], 'MarketCap':[], 'Price':[], 'EarningP':[],'MarketBeat':[]}) #analyzed with trades still open
    openArr = pd.DataFrame({'Stock':[], 'pprof':[], 'avgTradeP':[], 'nTrades':[],'avgDays':[],'openSeshs':[],'numOpen':[],'Industry':[],'Sector':[], 'MarketCap':[], 'Price':[], 'EarningP':[],'MarketBeat':[]}) #analyzed with trades still open
    restArr = pd.DataFrame({'Stock':[], 'pprof':[], 'avgTradeP':[], 'nTrades':[],'avgDays':[],'openSeshs':[],'numOpen':[],'Industry':[],'Sector':[], 'MarketCap':[], 'Price':[], 'EarningP':[],'MarketBeat':[]})
    cap = 100
    nSkipped = 0
    oldDat = pd.read_csv(('./outs/' + 'lastOpen.csv'))
    print("Analyzing %d stocks" % len(allTicks))
    for t in allTicks: #looping through each ticker and running the technical analysis
        print(t," ")            
        try: 
            bs, nSells, dOff, nOpen, fundDat, lastClose, marketBeat, trades, perfDat = tickerTesterV2(t,tFrame,inter,algo,pyd, cap) #calculate buy/sell signals and extract close prices
            if len(bs)!=0 and nSells!=0:
                # perfDat = perfCalcV2(bs,nSells, cap)    
                # score = scoreCalc(perfDat)
                # activityFactor = round(perfDat[2]*perfDat[6]/pAge*100,2)
                # earningPerc = round((perfDat[-1]-cap)/cap*100,2)
                isNew = True
                for oldT in oldDat['Stock']:
                    if t == oldT:
                        isNew = False
                        break

                if (nOpen > 0) and (dOff<perfDat[3]) and isNew: #
                    #               [t, %prof,    avgTrade,   ntrades,  avgOpenDays,dOff, nopen, industry,   sector,     marketCap,  price          earning percentage,       activity fact,     score]
                    newRow = {'Stock':t,'pprof':perfDat[0],'avgTradeP':perfDat[1],'nTrades':perfDat[2],'avgDays':perfDat[3],'openSeshs':dOff,'numOpen':nOpen,'Industry':fundDat[0],'Sector':fundDat[1],'MarketCap':fundDat[2],'Price':round(lastClose,2),'EarningP':round(perfDat[5],2),'MarketBeat':round(marketBeat,2)} #collecting outputted data into array
                    newArr.loc[len(newArr)] = newRow
                elif (nOpen > 0) and (dOff<perfDat[3]):
                                 #               [t, %prof,    avgTrade,   ntrades,  avgOpenDays,dOff, nopen, industry,   sector,     marketCap,  price          earning percentage,       activity fact,     score]
                    openRow = {'Stock':t,'pprof':perfDat[0],'avgTradeP':perfDat[1],'nTrades':perfDat[2],'avgDays':perfDat[3],'openSeshs':dOff,'numOpen':nOpen,'Industry':fundDat[0],'Sector':fundDat[1],'MarketCap':fundDat[2],'Price':round(lastClose,2),'EarningP':round(perfDat[5],2),'MarketBeat':round(marketBeat,2)} #collecting outputted data into array
                    openArr.loc[len(openArr)] = openRow
                else:
                    #               [t, %prof,    avgTrade,   ntrades,  avgOpenDays,dOff, nopen, industry,   sector,     marketCap,  price              realAvg,        ntFact,     score]
                    restRow = {'Stock':t,'pprof':perfDat[0],'avgTradeP':perfDat[1],'nTrades':perfDat[2],'avgDays':perfDat[3],'openSeshs':dOff,'numOpen':nOpen,'Industry':fundDat[0],'Sector':fundDat[1],'MarketCap':fundDat[2],'Price':round(lastClose,2),'EarningP':round(perfDat[5],2),'MarketBeat':round(marketBeat,2)} #collecting outputted data into array
                    restArr.loc[len(restArr)] = restRow
        except:
            print("Skipped")
            nSkipped += 1
            pass

    newArr = newArr.sort_values(by=['openSeshs'],ascending=True)
    openArr = openArr.sort_values(by=['openSeshs'],ascending=True)
    openArr = openArr.sort_values(by=['EarningP'],ascending=False)

    pd.set_option('display.max_columns', None)  
    pd.set_option('display.max_rows', None)  
    pd.set_option('display.expand_frame_repr', False)

    print("%d stocks skipped\n" % nSkipped)
    if len(newArr) == 0:
        print("\n No New Tickers: ----------------------------------------------------------------\n")
    else:
        print("\n New Stats: ----------------------------------------------------------------\n")
        print("avgPProf: ",newArr['pprof'].mean().round(2),"avgTradeP: ",newArr['avgTradeP'].mean().round(2),"avgNTrades: ",newArr['nTrades'].mean().round(2),"avgDays: ", newArr['avgDays'].mean().round(2), "avgEarningP: ", newArr['EarningP'].mean().round(2))
        print("\n New Tickers: ----------------------------------------------------------------\n")
        print(newArr)
        # newArr.to_csv(('./outs/' + algo + '_' + tdyDT + '_' + allFilt[0] + '_' + allFilt[1] + '_' + allFilt[2] + '_NEW.csv'))
        newArr.to_csv(('./outs/' + algo + '_' + tdyDT + '_' + allFilt[0] + '_' + allFilt[1] + '_NEW.csv'))


    if len(openArr) == 0:
        print("\n No Open Tickers: ----------------------------------------------------------------\n")
    else:
        print("\n Open Stats: ----------------------------------------------------------------\n")
        print("avgPProf: ",openArr['pprof'].mean().round(2),"avgTradeP: ",openArr['avgTradeP'].mean().round(2),"avgNTrades: ",openArr['nTrades'].mean().round(2),"avgDays: ", openArr['avgDays'].mean().round(2), "avgEarningP: ", openArr['EarningP'].mean().round(2))
        print("\n Open Tickers: ----------------------------------------------------------------\n")
        print(openArr)
        # openArr.to_csv(('./outs/' + algo + '_' + tdyDT + '_' + allFilt[0] + '_' + allFilt[1] + '_' + allFilt[2] + '_OPEN.csv'))
        openArr.to_csv(('./outs/' + algo + '_' + tdyDT + '_' + allFilt[0] + '_' + allFilt[1] + '_OPEN.csv'))


    print("\n Rest Stats: ----------------------------------------------------------------\n")
    print("avgPProf: ",restArr['pprof'].mean().round(2),"avgTradeP: ",restArr['avgTradeP'].mean().round(2),"avgNTrades: ",restArr['nTrades'].mean().round(2),"avgDays: ", restArr['avgDays'].mean().round(2), "avgEarningP: ", restArr['EarningP'].mean().round(2))
    print("\n Rest of Tickers: ----------------------------------------------------------------\n")
    print(restArr)
    # restArr.to_csv(('./outs/' + algo + '_' + tdyDT + '_' + allFilt[0] + '_' + allFilt[1] + '_' + allFilt[2] + '_REST.csv'))
    restArr.to_csv(('./outs/' + algo + '_' + tdyDT + '_' + allFilt[0] + '_' + allFilt[1] +'_REST.csv'))



    mergedArr = pd.concat([openArr, newArr], ignore_index=True, sort=False)
    mergedArr.to_csv(('./outs/' + 'lastOpen.csv'))


    sendEmail(newArr,openArr,dfClose)


schedule.every().monday.at("07:00").do(scheduledRunScript)
schedule.every().tuesday.at("07:00").do(scheduledRunScript)
schedule.every().wednesday.at("07:00").do(scheduledRunScript)
schedule.every().thursday.at("07:00").do(scheduledRunScript)
schedule.every().friday.at("07:00").do(scheduledRunScript)
# schedule.every().saturday.at("12:13").do(scheduledRunScript)

while True:
    schedule.run_pending()
    print("Run pending: ")
    # Sleep for 30 mins
    time.sleep(1800)
# scheduledRunScript()