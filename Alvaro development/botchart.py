from poloniex import poloniex
import urllib, json
import pprint
import datetime
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
				print "Checking the data from "+datetime.datetime.fromtimestamp(int(startTime)).strftime('%Y-%m-%d %H:%M:%S') + " to " + datetime.datetime.fromtimestamp(int(endTime)).strftime('%Y-%m-%d %H:%M:%S') 
				
				
				poloData = self.conn.api_query("returnChartData",{"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
				
				
				#A:poloData is an list (checked with the funtion type(), where each item of the list contains 4 values of the period 
				for datum in poloData:
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


	def getPoints(self):
		return self.data

	def getCurrentPrice(self):
		currentValues = self.conn.api_query("returnTicker")
		lastPairPrice = {}
		lastPairPrice = currentValues[self.pair]["last"]
		return lastPairPrice

	def chart(self, dataPoints):
		output = open("output.html",'w')
		output.truncate()
		output.write("""<html><head><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script><script type="text/javascript">google.charts.load('current', {'packages':['corechart']});google.charts.setOnLoadCallback(drawChart);function drawChart() {var data = new google.visualization.DataTable();data.addColumn('string', 'time');data.addColumn('number', 'value');data.addColumn({type: 'string', role:'annotation'});data.addColumn({type: 'string', role:'annotationText'});data.addColumn('number', 'trend');data.addRows([""")
		for point in dataPoints:
				output.write("['"+point['date']+"',"+point['price']+","+point['label']+","+point['desc']+","+point['trend'])
				output.write("],\n")
		output.write("""]);var options = {title: 'Price Chart',legend: { position: 'bottom' }};var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));chart.draw(data, options);}</script></head><body><div id="curve_chart" style="width: 100%; height: 100%"></div></body></html>""")
		exit()