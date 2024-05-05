import pandas as pd
import pandas_ta as ta
import yfinance as yf
import numpy as np


datArr = []

tkrs = pd.read_csv("./archive/stockList.txt")
# print(tkrs)
sList = np.array(tkrs.Tkr[:]) #Extracting tickers into a separate array
print(sList)

for tkr in sList:
	print(tkr)
	try:
		dat = yf.Ticker(tkr)
		dInfo = dat.info #Ticker info
		# print(dInfo)
		beta = dInfo['beta']
		tPE = dInfo['trailingPE']
		fPE = dInfo['forwardPE']
		tEPS = dInfo['trailingEps']
		fEPS = dInfo['forwardEps']
		datArr.append([tkr,beta,tPE,fPE,tEPS,fEPS])
	except:
		print('Skipped')
		datArr.append([tkr])
		pass

titles = ['Ticker','Beta','Trailing PE','Forward PE','Trailing EPS','Forward EPS']
df = pd.DataFrame(datArr,columns = titles)
df.to_csv('./archive/outData.csv')
