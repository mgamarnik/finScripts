import pandas as pd
import pandas_ta as ta
import yfinance as yf
import numpy as np
from diffPlus import diffPlus
import math

#Comparing performance of tkr in timeframes of buy/sell for ticker analyzed in bs

def baseline(bs,tkr,tFrame):

	dat = yf.Ticker(tkr)
	dInfo = dat.info #Ticker info
    # print(dInfo)
	df = dat.history(period = tFrame, interval = '1d') #Ticker Dataframe

    #Dataframe of close prices
	closes = df['Close']

	pDiffs = []
	i=0
	while i < (len(bs)-1):
		try: 
			buyClose = df.loc[bs.loc[i,"Date"],"Close"]
			sellClose = df.loc[bs.loc[i+1,"Date"],"Close"]
			baselineDiff = sellClose/buyClose-1
			# print(baselineDiff)
			stockDiff = bs.loc[i+1,"Price"]/bs.loc[i,"Price"]-1
			# print(stockDiff)
			perfDiff = stockDiff-baselineDiff
			# print(perfDiff)
			pDiffs = np.append(pDiffs,round(perfDiff*100,2))
		except:
			print("Out of date\n")

		i+=2


	return pDiffs
