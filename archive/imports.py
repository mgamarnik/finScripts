#Imports
def imports():
	import yfinance as yf
	import numpy as np
	# from sympy.matrices import Matrix 
	import scipy as sc
	import csv
	import matplotlib.pyplot as plt
	import pendulum
	import pandas as pd
	import pandas_ta as ta
	from datetime import datetime

	return (yf,np,sc,csv,plt,pendulum,pd,ta,datetime)