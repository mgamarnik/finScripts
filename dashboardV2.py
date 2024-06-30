import numpy as np
from tickerTester import tickerTester
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly as ply
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from diffPlus import diffPlus

#Plots candlestick stock price with 50 and 200 sma and buy/sell signals from ticker tester, Volume, MACD, and RSI all stacked together
def dashboardV2(tkr,tFrame,bs,algo):

	#Pull ticker data
	dat = yf.Ticker(tkr)
	df = dat.history(period = tFrame, interval = '1d') #Ticker Dataframe

	#run ticker tester to get buy/sells
	# bs, nSells, dOff, nOpen, fundDat, lastClose, pAge = tickerTester(tkr,tFrame,algo,pyd) #get bs as function input

	#Calc Moving Averages
	df['MA30'] = ta.sma(df['Close'],30)
	df['MA50'] = ta.sma(df['Close'],50)
	df['eMA50'] = ta.ema(df['Close'],50)
	df['MA200'] = ta.sma(df['Close'],200)
	df['eMA200'] = ta.ema(df['Close'],200)

	bbs = ta.bbands(df['Close'], length = 200, std=2)
	# print(bbs)

	df['bbU'] = bbs['BBU_200_2.0']
	df['bbM'] = bbs['BBM_200_2.0']
	df['bbL'] = bbs['BBL_200_2.0']

	atr = ta.atr(df['High'],df['Low'],df['Close'], length=50)
	df['atr50'] = atr
	df['datr50'] = diffPlus(atr,50)

	# volDiff = pd.DataFrame.diff(df['Volume'])
	# dVolSma = ta.sma(volDiff,length = 30)
	dVolSma = ta.ema(df['Volume'],length = 30)
	dVolSma = diffPlus(dVolSma,30)
	df['dVol_MA30'] = dVolSma

	#Calc MACD
	macd = ta.macd(df['Close'], fast=12, slow=26, signal=9, append=True)
	# print(macd)

	#Calc RSI
	rsi = ta.rsi(df['Close'], length=14)
	smaRSI = ta.sma(rsi,length=14)

	kst = ta.kst(df['Close'])

	buyMat = []
	sellMat = []

	if len(bs) != 0:
		#Extract buy/sell signals from BS array
		buyRows = bs[bs["Signal"]==0]
		# print(buyRows)
		sellRows = bs[bs["Signal"]==1]

		buyMat = pd.DataFrame({"BuyDate":buyRows["Date"],"BuyPrice":buyRows["Price"]})
		sellMat = pd.DataFrame({"SellDate":sellRows["Date"],"SellPrice":sellRows["Price"]})
	
	#Set scroll settings for ease of chart manipulation
	config = dict({'scrollZoom':True})

	#Fig definition
	fig=go.Figure()
	fig = ply.subplots.make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.01, row_heights=[0.4,0.2,0.2,0.2])
	
	#Candlestick Chart with moving averages at bottom---------------------------------------
	fig.add_trace(
			go.Candlestick(x=df.index,
	            open=df['Open'],
	            high=df['High'],
	            low=df['Low'],
	            close=df['Close'], name = 'market data'))
	# fig.add_trace(go.Scatter(x=df.index, y=df['MA30'], opacity=0.7, line=dict(color='green',width=2),name='MA30'))
	fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], opacity=0.7, line=dict(color='blue',width=2),name='MA50'))
	# fig.add_trace(go.Scatter(x=df.index, y=df['eMA50'], opacity=0.7, line=dict(color='blue',width=2),name='MA50'))
	fig.add_trace(go.Scatter(x=df.index, y=df['MA200'], opacity=0.7, line=dict(color='orange',width=2),name='MA200'))
	# fig.add_trace(go.Scatter(x=df.index, y=df['eMA200'], opacity=0.7, line=dict(color='orange',width=2),name='MA200'))

	# fig.add_trace(go.Scatter(x=df.index, y=df['bbU'], opacity=0.7, line=dict(color='gray',width=2),name='bbandUp'))
	# fig.add_trace(go.Scatter(x=df.index, y=df['bbM'], opacity=0.7, line=dict(color='gray',width=2),name='bbandMid'))
	# fig.add_trace(go.Scatter(x=df.index, y=df['bbL'], opacity=0.7, line=dict(color='gray',width=2),name='bbandLow'))

	symbols=['triangle_up']
	#Buy/Sell indicators on the same subchart-----------------------------------------------
	if len(buyMat) != 0:
		fig.add_trace(go.Scatter(x=buyMat['BuyDate'], y = buyMat['BuyPrice'], mode='markers+text', text="buy",textposition="bottom center", marker_symbol=5, marker_color='green', marker_size=15, name = 'buySignals'))
		fig.add_trace(go.Scatter(x=sellMat['SellDate'], y = sellMat['SellPrice'], mode= 'markers+text',text="sell",textposition="bottom center",marker_symbol=6,marker_color='red', marker_size=15, name = 'sellSignals'))

	# #Volume histogram------------------------------------------------------------------------
	# colorsV = ['green' if row['Open'] - row['Close'] >= 0 
	#           else 'red' for index, row in df.iterrows()]
	# fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=colorsV), row=1, col=1)


	#Volume dVol_MA
	# fig.add_trace(go.Scatter(x=df.index,y=df['dVol_MA30'],line=dict(color='orange',width=2)),row=2,col=1)
	# fig.add_trace(go.Scatter(x=df.index,y=df['datr50'],line=dict(color='orange',width=2)),row=2,col=1)
	
	# fig.add_trace(go.Scatter(x=df.index,y=df['datr50']+df['datr50'].std(),line=dict(color='blue',width=2)),row=2,col=1)
	# fig.add_trace(go.Scatter(x=df.index,y=df['datr50']-df['datr50'].std(),line=dict(color='blue',width=2)),row=2,col=1)

	fig.add_trace(go.Scatter(x=df.index,y=2*df['datr50'].rolling(50).std(),line=dict(color='green',width=2)),row=2,col=1)
	# fig.add_trace(go.Scatter(x=df.index,y=df['datr50']-df['datr50'].rolling(50).std(),line=dict(color='green',width=2)),row=2,col=1)
	
	hBars = pd.DataFrame({"Upper":np.ones(len(df.index))*0.005,"Lower":np.ones(len(df.index))*-0.005})
	fig.add_trace(go.Scatter(x=df.index,y=hBars["Upper"],line=dict(color='gray',width=1,dash='dash')),row=2,col=1)
	fig.add_trace(go.Scatter(x=df.index,y=hBars["Lower"],line=dict(color='gray',width=1,dash='dash')),row=2,col=1)

	# #MACD histogram and lines------------------------------------------------------------------
	# colorsH = ['green' if val >= 0 else 'red' for val in macd['MACDh_12_26_9']]
	# fig.add_trace(go.Bar(x=df.index, y=macd['MACDh_12_26_9'],marker_color=colorsH),row=3,col=1)
	# fig.add_trace(go.Scatter(x=df.index,y=macd['MACD_12_26_9'],line=dict(color='blue',width=2)),row=3,col=1)
	# fig.add_trace(go.Scatter(x=df.index,y=macd['MACDs_12_26_9'],line=dict(color='red',width=1)),row=3,col=1)




	#RSI lines and overbought/sold limits------------------------------------------------------
	hBars = pd.DataFrame({"Oversold":np.ones(len(df.index))*30,"Overbought":np.ones(len(df.index))*70})
	# print(hBars)
	fig.add_trace(go.Scatter(x=df.index,y=rsi,line=dict(color='purple',width=2)),row=3,col=1)
	fig.add_trace(go.Scatter(x=df.index,y=smaRSI,line=dict(color='yellow',width=2)),row=3,col=1)
	fig.add_trace(go.Scatter(x=df.index,y=hBars["Oversold"],line=dict(color='gray',width=1,dash='dash')),row=3,col=1)
	fig.add_trace(go.Scatter(x=df.index,y=hBars["Overbought"],line=dict(color='gray',width=1,dash='dash')),row=3,col=1)


	fig.add_trace(go.Scatter(x=df.index,y=kst["KST_10_15_20_30_10_10_10_15"],line=dict(color='green',width=2)),row=4,col=1)
	fig.add_trace(go.Scatter(x=df.index,y=kst["KSTs_9"],line=dict(color='red',width=2)),row=4,col=1)

	#axis updates
	fig.update_yaxes(title_text="Stock Price (USD per Shares)",autorange=True,fixedrange=False, row=1, col=1,)
	# fig.update_yaxes(title_text="Volume",autorange=True,fixedrange=False, row=2, col=1)
	fig.update_yaxes(title_text="Volume dMA30",autorange=True,fixedrange=False, showgrid=False, row=2, col=1)
	fig.update_yaxes(title_text="RSI",autorange=True,fixedrange=False, row=3, col=1)
	fig.update_yaxes(title_text="KST",autorange=True,fixedrange=False, row=4, col=1)



	#layout updates
	fig.update_layout(
	    title= tkr +' Live Share Price with buy/sell indicators for algo: '+algo,
	    showlegend=False,
	    template='plotly_dark')

	# x-axis button configurations
	fig.update_xaxes(
	    rangeslider_visible=False,
	    # rangeselector=dict(
	    #     buttons=list([
	    #         # dict(count=15, label="15m", step="minute", stepmode="backward"),
	    #         # dict(count=45, label="45m", step="minute", stepmode="backward"),
	    #         # dict(count=1, label="HTD", step="hour", stepmode="todate"),
	    #         dict(count=1, label="1m", step="month", stepmode="backward"),
	    #         dict(count=3, label="3m", step="month", stepmode="backward"),
	    #         dict(count=1, label="1y", step="year", stepmode="backward"),
	    #         dict(count=5, label="5y", step="year", stepmode="backward"),
	    #         dict(step="all")
	    #     ])
	    # )
	)



	fig.show(config=config)
