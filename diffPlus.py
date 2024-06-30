import numpy as np
import pandas as pd

def diffPlus(arr, tInt):

	arrLead = arr[tInt:len(arr)]
	datesLead = arr.index[tInt:len(arr)]
	# print(arrLead)
	arrLag = arr[0:len(arr)-tInt]
	# print(arrLag)
	# arrDiff = arrLead.sub(arrLag)
	arrDiff = np.array(arrLead)-np.array(arrLag)
	# print(arrDiff)
	dArr = arrDiff/tInt
	
	df = pd.DataFrame({'deriv': dArr},index=datesLead)
	# print(df)

	return df