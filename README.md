# code improvement:
- upgrade runscript to be its own function/clean up runscript
- figure out why so many tickers are skipped
- include market cap or other fundamental data in score calc? perhaps 2 scores, one technical one fundamental
- incorporate beta into score calc or as independent metric
- add "watchlist" section after open section in runscript output for stocks that are close to open
-  figure out better buy method rather than adding 10 for each buy and subtracting 1 per day
 - do proper trade comparing performance of doing >0 or >20 or >10 for buy threshold
- score heavily swayed by nTrades/nDaysHeld, ntrades and ndaysheld should be compared to industry average for that stock

# studies
- standardize method of doing studies, very unorganized now and untracible for the future
 - perform study, record result, implement change to master code or create new algo
- compare stock performance at every buy/sell to gspc buy/sell to see if trend exists
 - relate to how stock industry usually performs against market (matches, opposite, follows some other indicator like rates?)
- compare stock chart against industry etf to see if general market trend or company specific
- improve sell criteria, extended hold for if price is > sma 50 > sma200 at price divergence sell  position
 - change algo at sell point from price divergence to long hold
 - prior to running, figure out what set of data you want as output (industry specific averages within the sector? sector averages?)

# ideas:
- use ML or optimization to refine RSI, MACD, and other parameters to better fit specific stock being analyzed to maximize profit (maybe more of a study?)
- update volume buy signal to be divergence signal not just volume positive sma
- dmi or adx to asses price direction or strength
- also implement volatility based position sizing
- implement stock loss sell at 15% or some value (try with backtester first)
- use chatgpt to pull current news stories for the stock
- figure out if you can calculate fundamental data like beta, p/e or other at a point in stock history while doing backtesting to see if there is a clear trend
- perform portfolio level backtest on set of 1000 or so stocks, use perfCalcCash as starting point? (1000 bs arrays over 5 yr period, sparse matrix calc)
 - pull stock list
 - cut historic data to 10 years or time interval that exists for all stocks in list
 - calculate technical metrics (macd, rsi, vol etc.) for every day in history starting at oldest date
 - when buy signal arises, "purchase stock" and subtract value from total starting in bank
 - if multiple buy signals and only can choose 1, use score metric to ID best option
 - continue until today and record returns
 - compare against market or industry

# raspberrypi:
- fix vpn situation
- add title to email

# Notes:
- goal to capture divergence with multiple signals showing confirmation
- several losing positions were bought when indicators were relatively level for a period of time prior to the buy signal while price was in steady decline with now real show of momentum or divergence 
- to increase returns, rebalance portfolio to 75/25 etf/stock
 - become more consistent with buying/selling stock and increase stock portfolio size to diversify

# Sources:

# Done/archived:
- improve notetaking method, maybe use github project to track tasks/code fixes?
- figure out how to properly use github
 - develop new code/strat on pc, push to git, on raspberry pi pull from git to update
- study on how md hist derivative and second deriv look during buy and sell days
- searching rsi<30 is misleading since threshold for buy is at 32.5, thus missing some stocks
 - search at <30 and <40 to cover all bases
- evaluate losing positions and find commonalities
- save bbmd/rsi and type of search as separate daily sheets
- reorganize folder structure for investing
- fix md signal to be buy if crossover or has crossed over while below 0 line (applied to rsimd3, APPLY TO BBMD AND STUDY can be applied to tradingview codes first to test)
- fix rsimd3 so that rsimd doesnt have to be <32.5 when md cross-over, if rsi signal was positive within x days and md signal happens then overall buy signal (use i=0, and add +1 every time one of the buys occurs and subtract when time is out of range, if i=4 or whatever, then set to open in the table)
 - i.e. -create buy window that combines inputs from rsi, md, bb, volume
- add last close price to the chart
- dont add stock picks to table if number of open days exceeds average days of the trade or something similar
- perform study on performance of rsimd vs rsimd2
- implementing fix created in the tickerTester_reorg code
- create volume strategy and add it to rsimd4 for price divergence
- fix CLOSE TESTER AGAIN
- run algo over every stock in specific sectors to get average performance metrics that can be compared against

