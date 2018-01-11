import sys, getopt
import datetime
from time import mktime as mktime
class botVariables(object):
	def __init__(self):
		#for backtesting you need a start and endtime
		self.startTime=self.unixtime((2018, 1, 5, 0, 0))
		self.endTime=self.unixtime((2018, 1, 10, 0, 0))

		#pair and period for trading
		self.pair="USDT_BTC"
		self.period=300

		#variables to form a stategy
		self.movingAvPeriod = 5
		self.movingAvPeriod2 = 20
		self.RSIPeriod = 14

		self.BollNumOfStd=1.5
		self.BollPeriod=12

		self.initialInvestment = 100 #in euros

		self.stopLoss=300 #in the pair, for examle BTC_USD

		#Fees for trading, depending on the platform it can be 0.1% or 0.5%
		self.makeFee=0.0005 #0.1% of the buying fees
		self.takeFee=0.0005 #0.1% of the selling fees

		#api keys allowing realtime trading
		self.api_key_poloniex='RZPH057A-1L01XZUI-TL2ZCFLP-0QK92K9J'
		self.api_secret_poloniex='f50a8cd597bca93d33e997603b754277ac7e7e98e4ed4da37470f7d184639af089278633bbe9aac3e54da0042673823fcd3d8a5c34112396b4a158a9203ab698'



	def unixtime(self, time):
		# the time must be in the following form:  startTime=(2017, 1, 1, 0, 0)
		dt = datetime.datetime(time[0], time[1], time[2], time[3], time[4])
		# Example of Unix Timestamp:  1456442580
		return int(mktime(dt.timetuple()))
