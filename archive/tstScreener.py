from finviz.screener import Screener

allFilt = ['cap_smallover', 'geo_usa','ta_rsi_os30']  
stock_list = Screener(filters=allFilt, table='Performance', order='Market Cap')  # Get the performance table and sort it by price ascending


# # Export the screener results to .csv
# stock_list.to_csv("stock.csv")

# tkrList = []
# for stock in stock_list:  # Loop through 10th - 20th stocks
# 	tkrList.append(stock['Ticker'])
# 	print(stock['Ticker'], stock['Price']) # Print symbol and price


# print(tkrList)
