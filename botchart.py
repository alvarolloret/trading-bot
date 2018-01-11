from poloniex import poloniex
import urllib, json
import pprint
import datetime
from botcandlestick import BotCandlestick
from botvariables import botVariables
from botindicators import BotIndicators
from bottrade import BotTrade
from bothtml import BotHTML

class BotChart(object):




	#------------------------------------------------------------------#
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
			print 'Ecxhange with Poloniex'
			self.conn = poloniex(self.api_key,self.api_secret)
			if backtest:
				print "Checking the data from "+datetime.datetime.fromtimestamp(int(startTime)).strftime('%Y-%m-%d %H:%M:%S') + " to " + datetime.datetime.fromtimestamp(int(endTime)).strftime('%Y-%m-%d %H:%M:%S')


				self.poloData = self.conn.api_query("returnChartData",{"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})


				#A:poloData is an list (checked with the funtion type(), where each item of the list contains 6 values of the period
				for datum in self.poloData:
					#datum is a dict = {key1:value1, key2:value2, ... }
					if (datum['open'] and datum['close'] and datum['high'] and datum['low']):
						#putting all this data to the BotCandlestick object
						self.data.append(BotCandlestick(self.period,datum['open'],datum['close'],datum['high'],datum['low'],datum['weightedAverage'], datum['date']))

		if (exchange == "bittrex"):
			if backtest:
				url = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName="+self.pair+"&tickInterval="+self.period+"&_="+str(self.startTime)
				response = urllib.urlopen(url)
				rawdata = json.loads(response.read())

				self.data = rawdata["result"]
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
				priceData.append(lastPairPrice)
				movingAverage=self.indicators.movingAverage(priceData,self.vars.movingAvPeriod,lastPairPrice)
				movingAverage2=self.indicators.movingAverage(priceData,self.vars.movingAvPeriod2,lastPairPrice)

				label=nextDataPoint.label
				dataDate = datetime.datetime.fromtimestamp(int(nextDataPoint.date)).strftime('%Y-%m-%d %H:%M:%S')
				#adding the trades on the label


			#step 2: once the iteration is finished, adding all the info in the chart
			elif(self.startTime and not historicalData):
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
				priceData.append(lastPairPrice)
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
