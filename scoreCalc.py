import numpy as np
import math

def scoreCalc(perfDat):
	#perfDat: [pProf, avgTrade, len(perf),oDate,bs,perf,avgDays]
	pProf = perfDat[0]
	avgTrade = perfDat[1]
	nTrades = perfDat[2]
	avgDays = perfDat[6]
	
	realAvg = pProf/100*avgTrade/100
	ntFact = nTrades/avgDays
	score = ntFact*realAvg*100

	stats = [round(realAvg,3),round(ntFact,3),round(score,2)]


	return	stats
