from poloniex import poloniex
import urllib, json
import pprint
from botcandlestick import BotCandlestick

class BotChart(object):
	def __init__(self, exchange, pair, period, startTime, endTime, backtest=True):
		self.pair = pair
		self.period = period

		self.startTime = startTime
		self.endTime = endTime
		self.api_key='RZPH057A-1L01XZUI-TL2ZCFLP-0QK92K9J'
		self.api_secret='f50a8cd597bca93d33e997603b754277ac7e7e98e4ed4da37470f7d184639af089278633bbe9aac3e54da0042673823fcd3d8a5c34112396b4a158a9203ab698'
		self.data = []
		
		if (exchange == "poloniex"):
			print 'Ecxhange with Poloniex'
			
			self.conn = poloniex(self.api_key,self.api_secret)

			if backtest:
				poloData = self.conn.api_query("returnChartData",{"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
				
				
				#A:poloData is an list (checked with the funtion type(), where each item of the list contains 4 values of the period 
				for datum in poloData:
					#datum is a dict = {key1:value1, key2:value2, ... }
					if (datum['open'] and datum['close'] and datum['high'] and datum['low']):
						#putting all this data to the BotCandlestick object
						self.data.append(BotCandlestick(self.period,datum['open'],datum['close'],datum['high'],datum['low'],datum['weightedAverage']))

		if (exchange == "bittrex"):
			if backtest:
				url = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName="+self.pair+"&tickInterval="+self.period+"&_="+str(self.startTime)
				response = urllib.urlopen(url)
				rawdata = json.loads(response.read())

				self.data = rawdata["result"]


	def getPoints(self):
		return self.data

	def getCurrentPrice(self):
		currentValues = self.conn.api_query("returnTicker")
		lastPairPrice = {}
		lastPairPrice = currentValues[self.pair]["last"]
		return lastPairPrice
