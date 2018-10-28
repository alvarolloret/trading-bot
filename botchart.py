#from exchange import poloniex
import poloniex
import urllib.request, urllib.parse, urllib.error, json
import pprint
import datetime
from botcandlestick import BotCandlestick
from botvariables import botVariables
from botindicators import BotIndicators
from bottrade import BotTrade
from bothtml import BotHTML
from binance.client import Client

class BotChart(object):



	#------------------------------------------------------------	------#
	#---------Part 1.1: Fetch the data from market---------------------#
	#------------------------------------------------------------------#
	#---Output: self.data=[Botcandlstck1 ,Botcandlestick2, ..3, ..4]---#
	#------------------------------------------------------------------#
	#------------------------------------------------------------------#
	def __init__(self, exchange, pair, period, startTime, endTime, backtest=True):
		self.botHTML=BotHTML()
		self.vars=botVariables()
		self.api_key=self.vars.api_key_poloniex
		self.api_secret=self.vars.api_secret_poloniex
		self.avPeriod=self.vars.movingAvPeriod
		self.indicators = BotIndicators()
		self.pair = pair
		self.period = period
		self.startTime = startTime
		self.endTime = endTime
		self.data = []
		self.prices = []
		self.poloData=[]
		self.trades=[]
		if (exchange == "poloniex"):
			print('Ecxhange with Poloniex')
			self.conn = poloniex.Poloniex(self.api_key,self.api_secret)
			if backtest:
				print("Checking the data from "+datetime.datetime.fromtimestamp(int(startTime)).strftime('%Y-%m-%d %H:%M:%S') + " to " + datetime.datetime.fromtimestamp(int(endTime)).strftime('%Y-%m-%d %H:%M:%S'))


				self.poloData = self.conn.returnChartData(self.pair,self.period,self.startTime,self.endTime)


				#A:poloData is an list (checked with the funtion type(), where each item of the list contains 6 values of the period
				for datum in self.poloData:
					#datum is a dict = {key1:value1, key2:value2, ... }
					if (datum['open'] and datum['close'] and datum['high'] and datum['low']):
						#putting all this data to the BotCandlestick object
						self.data.append(BotCandlestick(self.period,datum['open'],datum['close'],datum['high'],datum['low'],datum['weightedAverage'], datum['date']))

		if (exchange == "binance"):
			# Remember to install binance python script with --> pip install python-binance
			print('Ecxhange with Binance')
			if backtest:
				# create the Binance client, no need for api key
				client = Client("", "")
				klines = client.get_historical_klines(self.vars.pairBinance, getattr(client, self.vars.periodBinance), self.vars.startTimeBinance, self.vars.endTimeBinance)
				for kline in klines:
					self.data.append(BotCandlestick(self.period,kline[1],kline[4],kline[2],kline[3],str((float(kline[1])+float(kline[2])+float(kline[4])+float(kline[3]))/4), int(((kline[0])+(kline[6]))/2000))) #because in miliseconds


				"""
				Get Historical Klines from Binance
			    [
				  [
				    1499040000000,      // 0.Open time 1517803200000
				    "0.01634790",       // 1.Open
				    "0.80000000",       // 2.High
				    "0.01575800",       // 3.Low
				    "0.01577100",       // 4.Close
				    "148976.11427815",  // 5.Volume
				    1499644799999,      // 6.Close time
				    "2434.19055334",    // 7.Quote asset volume
				    308,                // 8.Number of trades
				    "1756.87402397",    // 9.Taker buy base asset volume
				    "28.46694368",      // 10.Taker buy quote asset volume
				    "17928899.62484339" // Ignore.
				  ]
				]
			    """
		# d = self.data[0].__dict__
		# print (d)

	#------------------------------------------------------------------#
	#---------END--Part 1.1: initialisating the bot strategy-----------#
	#------------------------------------------------------------------#






	#--------------------------------------------------------------#
	#---------Part 1.3: Evaluating each candlestic from the chart--#
	#--------------------------------------------------------------#
	#--------------------USING THE STRATEGY TICK-------------------#
	#--------------------------------------------------------------#
	def getPoints(self):
		return self.data







	def getCurrentPrice(self):
		currentValues = self.conn.api_query("returnTicker")
		lastPairPrice = {}
		lastPairPrice = currentValues[self.pair]["last"]
		return lastPairPrice

	def getLastPrices(self,date,dataCandlestick,period):
		lastPrices=[]
		#https://stackoverflow.com/a/3940144/5176549
		for candlestick in reversed(dataCandlestick):
			lastPrices.append(candlestick['weightedAverage'])
			if date == (candlestick['date']):
				break
		return lastPrices[-period:]

	def createChart(self):
		historicalData=self.data
		dataPoints = []
		priceData=[]
		label='null'
		output = open("output.html",'w')
		output.truncate()
		#Understanding googlechart: https://developers.google.com/chart/interactive/docs/basic_load_libs
		output.write(self.botHTML.begin)

		while True:
			#step 0: iterating over data points
			if (self.startTime and historicalData):
				nextDataPoint = historicalData.pop(0)  #https://stackoverflow.com/a/4426727/5176549
				lastPairPrice = nextDataPoint.priceAverage
				priceData.append(float(lastPairPrice))
				movingAverage=self.indicators.movingAverage(priceData,self.vars.movingAvPeriod,lastPairPrice)
				movingAverage2=self.indicators.movingAverage(priceData,self.vars.movingAvPeriod2,lastPairPrice)
				label=nextDataPoint.label
				dataDate = datetime.datetime.fromtimestamp(int(nextDataPoint.date)).strftime('%Y-%m-%d %H:%M:%S')
				#adding the trades on the label

			#step 2: once the iteration is finished, adding all the info in the chart
			elif(self.startTime and not historicalData):
				print ("Finished")
				for point in dataPoints:
					output.write("["+self.stringToDate(point['date'])+","+point['price']+","+point['label']+","+point['desc']+","+point['movAv1']+","+point['movAv2'])
					output.write("],\n")
				output.write(self.botHTML.end)
				break

			#step 1: addind the last point on the list
			else:
				currentValues = conn.api_query("returnTicker")
				lastPairPrice = currentValues[pair]["last"]
				dataDate = datetime.datetime.now()

			#Main step: appending values to local dataPoints
			dataPoints.append({
			'date':dataDate,
			'price': str(lastPairPrice),
			'movAv1': str(movingAverage),
			'movAv2': str(movingAverage2),
			'label': label,
			'desc': 'null'})


	def stringToDate(self , date):
		#date is the follwing format: date='2017-12-27 11:50:00'
		return "new Date("+date[0:4]+", "+date[5:7]+", "+date[8:10]+", "+date[11:13]+", "+date[14:16]+")"


	def creatChartRSI(self):
		#Double Chart zoom: https://stackoverflow.com/a/42238747/5176549 or https://jsfiddle.net/pzamu7kt/
		#Understanding googlechart: https://developers.google.com/chart/interactive/docs/basic_load_libs
		historicalData=self.data
		dataPoints = []
		priceData=[]
		movingAverage=0
		label='null'
		output = open("outputrsi.html",'w')
		output.truncate()
		#Understanding googlechart: https://developers.google.com/chart/interactive/docs/basic_load_libs
		output.write(self.botHTML.javascript)


		while True:
			#step 0: iterating over data points
			if (self.startTime and historicalData):
				nextDataPoint = historicalData.pop(0)
				#https://stackoverflow.com/a/4426727/5176549
				lastPairPrice = nextDataPoint.priceAverage
				priceData.append(float(lastPairPrice))
				BollUp=self.indicators.BollUp(priceData,self.vars.BollPeriod,lastPairPrice)
				BollDown=self.indicators.BollDown(priceData,self.vars.BollPeriod,lastPairPrice)
				rsiData=self.indicators.RSI(priceData)
				label=nextDataPoint.label
				dataDate = datetime.datetime.fromtimestamp(int(nextDataPoint.date)).strftime('%Y-%m-%d %H:%M:%S')
				#adding the trades on the label


			#step 2: once the iteration is finished, adding all the info in the chart
			elif(self.startTime and not historicalData):
				output.write(self.botHTML.chart11)
				for point in dataPoints:
					output.write("["+self.stringToDate(point['date'])+","+point['price']+","+point['label']+","+point['desc']+","+point['BollUp']+","+point['BollDown'])
					output.write("],\n")
				output.write(self.botHTML.chart12)
				output.write(self.botHTML.chart21)
				for point in dataPoints:
					# print (point['rsi'])
					output.write("["+self.stringToDate(point['date'])+","+point['rsi'])
					output.write("],\n")
				output.write(self.botHTML.chart22)
				output.write(self.botHTML.endjavascript)
				break

			#step 1: addind the last point on the list
			else:
				currentValues = conn.api_query("returnTicker")
				lastPairPrice = currentValues[pair]["last"]
				dataDate = datetime.datetime.now()

			#Main step: appending values to local dataPoints
			dataPoints.append({
			'date':dataDate,
			'price': str(lastPairPrice),
			'BollUp': str(BollUp),
			'BollDown': str(BollDown),

			'rsi': str(rsiData),
			'label': label,
			'desc': 'null'})
