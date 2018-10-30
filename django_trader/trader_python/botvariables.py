import sys, getopt
import datetime
from time import mktime as mktime
import time

class botVariables(object):
	def __init__(self):
		#self.market
		self.market="binance" 	#options: binance, poloniex
		self.backtest=True

		#for backtesting you need a start and endtime
		if (self.market=="binance"):
			self.pair='ETHUSDT'	#For binance
			self.period="KLINE_INTERVAL_4HOUR" 	#For binance: KLINE_INTERVAL_12HOUR, 15MINUTE, 1DAY, 1HOUR, 1MINUTE, ETC, see : https://python-binance.readthedocs.io/en/latest/binance.html
			self.startTime=str(mktime(time.strptime('2018-02-01 17:00:00', '%Y-%m-%d %H:%M:%S')))
			self.endTime=str(mktime(time.strptime('2018-06-01 17:00:00', '%Y-%m-%d %H:%M:%S')))
		elif (self.market=="poloniex"):
			self.pair="USDT_ETH"     	#For poloniex
			self.period=14400  			#Poloniex: In seconds, valid values are 300, 900, 1800, 7200 (2h), 14400 (4h), and 86400 (1d)
			self.startTime=self.unixtime((2018, 2, 1, 0, 0)) #poloniex
			self.endTime=self.unixtime((2018, 6, 1, 0, 0)) #poloniex








		#variables to form a stategy



		self.movingAvPeriod = 15
		self.movingAvPeriod2 = 50
		self.RSIPeriod = 4

		self.BollNumOfStd=2
		self.BollPeriod=12

		self.initialInvestment = 100 #in euros

		self.stopLoss=300 #in the pair, for examle BTC_USD

		#Fees for trading, depending on the platform it can be 0.1% or 0.5%
		self.makeFee=0.0005 #0.1% of the buying fees
		self.takeFee=0.0005 #0.1% of the selling fees

		#api keys allowing realtime trading
		self.api_key_poloniex='-'
		self.api_secret_poloniex='-'



	def unixtime(self, time):
		# the time must be in the following form:  startTime=(2017, 1, 1, 0, 0)
		dt = datetime.datetime(time[0], time[1], time[2], time[3], time[4])
		# Example of Unix Timestamp:  1456442580
		return int(mktime(dt.timetuple()))

	def modifyStartTime(self, time1):
		# the time must be in the following form:  startTime=(2017, 1, 1, 0, 0)
		self.startTime=time1


	def modifyEndTime(self, time2):
		# the time must be in the following form:  startTime=(2017, 1, 1, 0, 0)
		self.endTime=time2
