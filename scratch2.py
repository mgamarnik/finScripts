from datetime import date
today = date.today()
tdyDT = today.strftime("%b_%d_%Y") 
print(tdyDT+"_openTrades.csv")
print()