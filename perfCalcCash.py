

import numpy as np

def perfCalc(bs,nSells):

    oDate = []
    perf = []
    nProf = 0
    pProf = 0
    avgTrade = 0
    avgDays = 0
    cap = 100 ##USE THIS CODE AS BASIS TO DO PORTFOLIO LEVEL BACKTEST NOT JUST STOCK LEVEL


    #Algorithm Performance Calculator ------------------------------------------------------------------------------

    if len(bs)>0: #if buy/sell signals exist
        
        if bs[-1][0] == 0 : #if the last signal was a buy. used to include (and the most recent close price was <= to the buy price "closes<=bs[-1][1]")
            oDate = bs[-1] #record the latest buy signal (THESE LINES DETERMINE WHICH STOCKS GET PUT INTO THE OPENARR)

        if nSells > 0: #if number of sells are greater than zero (open buy signal may be the only signal)
            buys = [] #array to assembly all buy signals corresponding to the sell signal
            sp = 0
            #assembling corresponding buy and sell signals to calculate performance
            for j in range(len(bs)):
                if bs[j][0] == 0:
                    buys.append([bs[j][1],bs[j][2],bs[j][3]]) #assembling buys
                else:
                    spp = bs[j][1] #sell price
                    spt = bs[j][2] #sell time
                    spidx = bs[j][3] #sell index
                    # if len(buys)==3: #FOR NBUYS STUDY ONLY
                    avgChange = 0
                    for bp in buys: 
                        bpp = bp[0] #buy price
                        bpt = bp[1] #buy time
                        bpidx = bp[2] #buy index
                        # if (spidx>bpidx) and (bp[3] == False): #PRICE POSITION STUDY ONLY, true means offset buy <og buy, false means offset buy>og buy
                        if spidx>bpidx:
                            net = spp-bpp #change in price
                            pdiff = (spp-bpp)/bpp*100 #pdiff between sell and buy
                            avgChange = (avgChange+spp/bpp)/avgChange if avgChange!=0 else spp/bpp
                            perf.append([[net],[pdiff],[bpp],[spp],[spidx-bpidx]]) #net change in price, percent difference, buy price, sell price
                    buys = [] #array to assembly all buy signals corresponding to the sell signal
                    cap = cap*(avgChange)



            if len(perf) != 0:
                #calculations for average trade profit, number of profitable trades, 
                avgTrade = round(np.mean(np.array(perf)[:,1]),2)
                nProf = sum(np.ceil(np.array(perf)[:,0]/max(abs(np.array(perf)[:,0]))))
                pProf = (nProf/len(np.array(perf)[:,0]))*100
                pProf = round(pProf[0],2)  
                avgDays = round(np.mean(np.array(perf)[:,4]),2)  
            else:
                #setting performance metrics to zero
                avgTrade = '0'
                nProf = '0'
                pProf = '0' 
            
            # print(perf)

    else: 
        #setting performance metrics to zero
        avgTrade = '0'
        nProf = '0'
        pProf = '0' 

    return [pProf, avgTrade, len(perf), oDate, bs, perf, avgDays, cap] #Percent Profitability, Average Trade Percentage, Number of Trades, latest buy signal, buy/sell array, perf array