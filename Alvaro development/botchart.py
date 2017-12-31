from poloniex import poloniex
import urllib, json
import pprint
import datetime
from botcandlestick import BotCandlestick
from botvariables import botVariables
from botindicators import BotIndicators
from bottrade import BotTrade

class BotChart(object):




	#------------------------------------------------------------------#
	#---------Part 1.1: Fetch the data from market---------------------#
	#------------------------------------------------------------------#
	#---Output: self.data=[Botcandlstck1 ,Botcandlestick2, ..3, ..4]---#
	#------------------------------------------------------------------#
	#------------------------------------------------------------------#
	def __init__(self, exchange, pair, period, startTime, endTime, backtest=True):
		self.vars=botVariables()
		self.api_key=self.vars.showApiKey()
		self.api_secret=self.vars.showApiSecret()
		self.avPeriod=self.vars.showMovAvPeriod()
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
				
				
				#A:poloData is an list (checked with the funtion type(), where each item of the list contains 4 values of the period 
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
		
	def createChart(self,trades):
		self.trades=trades
		historicalData=self.poloData
		dataPoints = []
		movingAverages=[]
		movingAverage=0
		tradeCompleted=0 #a trade is completed when it sums 2 --> 1 for buy & 1 for sell
		numOfTrades=0
		label='null'
		output = open("output.html",'w')
		output.truncate()
		#Understanding googlechart: https://developers.google.com/chart/interactive/docs/basic_load_libs
		output.write("""<html><head><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
		<script type="text/javascript">google.charts.load('current', {'packages':['corechart']});
		google.charts.setOnLoadCallback(drawChart);
		function drawChart() 
		{var data = new google.visualization.DataTable();
		data.addColumn('string', 'time');
		data.addColumn('number', 'value');
		data.addColumn({type: 'string', role:'annotation'});
		data.addColumn({type: 'string', role:'annotationText'});
		data.addColumn('number', 'movingAverage');
		data.addRows([""")
		
		while True:
			#step 0: iterating over data points
			if (self.startTime and historicalData):
				nextDataPoint = historicalData.pop(0)  #https://stackoverflow.com/a/4426727/5176549
				lastPairPrice = nextDataPoint['weightedAverage']
				movingAverages.append(lastPairPrice)
				movingAverage=self.indicators.movingAverage(movingAverages,self.vars.movingAvPeriod,lastPairPrice)
				dataDate = datetime.datetime.fromtimestamp(int(nextDataPoint['date'])).strftime('%Y-%m-%d %H:%M:%S')
				#adding the trades on the label
				
				# if (not not trades) and int(trades[0].entryTime)==int(nextDataPoint['date']):
					# label="'Buy'"
					# tradeCompleted+=1
				# elif (not not trades) and int(trades[0].exitTime)==int(nextDataPoint['date']):
					# label="'Sell'"
					# tradeCompleted+=1
				# elif (not not trades) and tradeCompleted==2:
					# trades.pop(0)
					# tradeCompleted=0
					# numOfTrades+=1
					# label='null'
				# else:
					# label='null'
				
				
			#step 2: adding all the info in the chart
			elif(self.startTime and not historicalData):
				for point in dataPoints:
					output.write("['"+point['date']+"',"+point['price']+","+point['label']+","+point['desc']+","+point['trend'])
					output.write("],\n")
				output.write("""]);
				var options = {title: 'Price Chart',legend: { position: 'bottom' }};
				var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
				chart.draw(data, options);
				}</script></head>
				<body><div id="curve_chart" style="width: 100%; height: 100%"></div></body>
				</html>""")
				print "NnumOfTrades: "+str(numOfTrades)+" num2 of points: "+str(len(dataPoints))
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
			'trend': str(movingAverage),
			'label': label,
			'desc': 'null'})
			
			
