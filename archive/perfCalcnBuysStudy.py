
import numpy as np

def perfCalc(bs,closes,nSells):

    oDate = []
    perf = []
    nProf = 0
    pProf = 0
    avgTrade = 0

    #Algorithm Performance Calculator ------------------------------------------------------------------------------

    if len(bs)>0: #if buy/sell signals exist
        if bs[-1][0] == 0 and closes[-1]<=bs[-1][1]: #if the last signal was a buy and the most recent close price was <= to the buy price
            oDate = bs[-1] #record the latest buy signal
        if nSells > 0: #if number of sells are greater than zero (open buy signal may be the only signal)
            buys = [] #array to assembly all buy signals corresponding to the sell signal
            sp = 0
            #assembling corresponding buy and sell signals to calculate performance
            for j in range(len(bs)):
                if bs[j][0] == 0:
                    buys.append([bs[j][1],bs[j][2]]) #assembling buys
                else:
                    spp = bs[j][1] #sell price
                    spt = bs[j][2] #sell time
                    for bp in buys:
                        bpp = bp[0] #buy price
                        bpt = bp[1] #buy time
                        net = spp-bpp #change in price
                        pdiff = (spp-bpp)/bpp*100 #pdiff between sell and buy
                        perf.append([[net],[pdiff],[bpp],[spp]]) #net change in price, percent difference, buy price, sell price
                    buys = []

            #calculations for average trade profit, number of profitable trades, 
            avgTrade = round(np.mean(np.array(perf)[:,1]),2)
            nProf = sum(np.ceil(np.array(perf)[:,0]/max(abs(np.array(perf)[:,0]))))
            pProf = (nProf/len(np.array(perf)[:,0]))*100
            pProf = round(pProf[0],2)    
    else: 
        #setting performance metrics to zero
        avgTrade = '0'
        nProf = '0'
        pProf = '0' 

    return [pProf, avgTrade, len(perf), oDate, bs, perf] #Percent Profitability, Average Trade Percentage, Number of Trades, latest buy signal, buy/sell array, perf array