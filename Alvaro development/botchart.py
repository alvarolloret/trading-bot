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
		movingAverages=[]
		movingAverage=0
		label='null'
		output = open("output.html",'w')
		output.truncate()
		#Understanding googlechart: https://developers.google.com/chart/interactive/docs/basic_load_libs
		output.write("""<html><head><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
		<script type="text/javascript">google.charts.load('current', {'packages':['corechart']});
		google.charts.setOnLoadCallback(drawChart);
		function drawChart() 
		{var data = new google.visualization.DataTable();
		data.addColumn('datetime', 'Date');
		data.addColumn('number', 'value');
		data.addColumn({type: 'string', role:'annotation'});
		data.addColumn({type: 'string', role:'annotationText'});
		data.addColumn('number', 'movingAverage');
		data.addColumn('number', 'movingAverage2');
		data.addRows([""")
		
		while True:
			#step 0: iterating over data points
			if (self.startTime and historicalData):
				nextDataPoint = historicalData.pop(0)  #https://stackoverflow.com/a/4426727/5176549
				lastPairPrice = nextDataPoint.priceAverage
				movingAverages.append(lastPairPrice)
				movingAverage=self.indicators.movingAverage(movingAverages,self.vars.movingAvPeriod,lastPairPrice)
				movingAverage2=self.indicators.movingAverage(movingAverages,self.vars.movingAvPeriod2,lastPairPrice)
				label=nextDataPoint.label
				dataDate = datetime.datetime.fromtimestamp(int(nextDataPoint.date)).strftime('%Y-%m-%d %H:%M:%S')
				#adding the trades on the label
				
				
			#step 2: once the iteration is finished, adding all the info in the chart
			elif(self.startTime and not historicalData):
				for point in dataPoints:
					output.write("["+self.stringToDate(point['date'])+","+point['price']+","+point['label']+","+point['desc']+","+point['movAv1']+","+point['movAv2'])
					output.write("],\n")
				output.write("""]);
				var options = {title: 'Price Chart',
				hAxis: {format: 'MMM, dd, yyyy, HH:mm'},
				explorer: {actions: ['dragToZoom', 'rightClickToReset'],axis: 'horizontal',maxZoomIn: 100.0},
				legend: { position: 'bottom' }};
				var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
				chart.draw(data, options);
				}</script></head>
				<body><div id="curve_chart" style="width: 100%; height: 70%"></div></body>
				</html>""")
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
		
		
	def creatChartRSI(self,data,RSIdata):
		historicalData=self.data
		dataPoints = []
		label='null'
		output = open("output.html",'w')
		output.truncate()
		#Double Chart zoom: https://stackoverflow.com/a/42238747/5176549 or https://jsfiddle.net/pzamu7kt/
		#Understanding googlechart: https://developers.google.com/chart/interactive/docs/basic_load_libs
		output.write("""<html><head><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
		<script type="text/javascript">
		google.charts.load('current', {
		callback: function () {
		var chart1;
		var chart2;

		var data1 = new google.visualization.DataTable();
		var data2 = new google.visualization.DataTable();

		var container1 = document.getElementById('mcs-chart');
		var container2 = document.getElementById('snr-chart');

		var outDiv1 = document.getElementById('mcs-chart-event');
		var outDiv2 = document.getElementById('snr-chart-event');

		var options1 = {title:'Wot',
		height:300,
		displayAnnotations: false,
		displayZoomButtons: false,
		chartArea: { width:'95%',height:'90%'},
		lineWidth: 1.5,
		legend: { position: 'none' },
		crosshair: {
		trigger: 'both',
		orientation: 'vertical'
		},
		explorer: {
		actions: ['dragToZoom', 'rightClickToReset'],
		axis: 'horizontal',
		keepInBounds: true,
		maxZoomIn: 10.0
		},
		};

		var options2 = {
		displayZoomButtons: false,
		displayRangeSelector: false,
		title:'rsi typ',
		chartArea: { width:'95%',height:'90%'},
		height:100,
		lineWidth: 1.5,
		colors: ['red'],
		legend: { position: 'none' },
		crosshair: {
		trigger: 'both',
		orientation: 'vertical'
		},
		explorer: {
		actions: ['dragToZoom', 'rightClickToReset'],
		axis: 'horizontal',
		keepInBounds: true,
		maxZoomIn: 10.0
		},
		};

		drawChartOne(data1);
		drawChartTwo(data2);

		google.visualization.events.addListener(chart1, 'onmouseover', function(selection) {
		chart1.setSelection(selection);
		chart2.setSelection([{ row: selection.row, column: null }]);
		});

		// sync chart2
		var observer = new MutationObserver(function () {
		setRange(getCoords());
		});

		// start observing on 'ready'
		google.visualization.events.addListener(chart1, 'ready', function() {
		observer.observe(container1, {
		childList: true,
		subtree: true
		});
		});

		google.visualization.events.addListener(chart2, 'onmouseover', function(selection) {
		chart2.setSelection(selection);
		chart1.setSelection([{ row: selection.row, column: null }]);
		});

		drawCharts();
		window.addEventListener('resize', drawCharts, false);
		function drawCharts() {
		chart1.draw(data1, options1);
		chart2.draw(data2, options2);
		}

		function drawChartOne(data) {
		data.addColumn('date', 'Date');
		data.addColumn('number', 'Sessions');
		data.addColumn({type: 'string', role: 'style'});
		data.addColumn({type:'string', role:'annotation'});

		var sessions = [786, 450, 866, 814, 192, 466, 984, 780, 922, 458, 786, 758, 701, 831, 901, 557, 114, 393, 689, 658, 103, 837, 164, 727, 593, 193, 945, 583, 948, 338];
		var start = new Date(1458345600 * 1000);
		var date;

		var dates = [];

		for(var i = 0; i < sessions.length; i++) {
		var newDate = start.setDate(start.getDate() + 1);
		if(i == 10){
		data.addRow([new Date(newDate), sessions[i],'point { size: 6; shape-type: circle; fill-color: green;','Buy']);

		}else{
		data.addRow([new Date(newDate), sessions[i],null,null]);
		}

		}

		chart1 = new google.visualization.LineChart(container1);
		}

		function drawChartTwo(data) {
		data.addColumn('date', 'Date');
		data.addColumn('number', 'Other Sessions');

		var rsi = [100, 450, 200, 333, 192, 466, 984, 77, 922, 458, 200, 758, 701, 831, 901, 557, 114, 393, 500, 658, 103, 837, 300, 727, 593, 193, 945, 583, 948, 338];

		var start = new Date(1458345600 * 1000);
		var date;

		for(var i = 0; i < rsi.length; i++) {
		var newDate = start.setDate(start.getDate() + 1);
		data.addRow([new Date(newDate), rsi[i]]);
		}

		chart2 = new google.visualization.LineChart(container2);
		}

		// get axis coordinates from chart1
		function getCoords() {
		var chartLayout = chart1.getChartLayoutInterface();
		var chartBounds = chartLayout.getChartAreaBoundingBox();
		return {
		x: {
		min: chartLayout.getHAxisValue(chartBounds.left),
		max: chartLayout.getHAxisValue(chartBounds.width + chartBounds.left)
		},
		y: {
		min: chartLayout.getVAxisValue(chartBounds.top),
		max: chartLayout.getVAxisValue(chartBounds.height + chartBounds.top)
		}
		};
		}

		// set axis coordinates on chart2
		function setRange(coords) {
		options2.hAxis = {};
		options2.vAxis = {};
		options2.hAxis.viewWindow = {};
		options2.vAxis.viewWindow = {};
		if (coords) {
		options2.hAxis.viewWindow.min = coords.x.min;
		options2.hAxis.viewWindow.max = coords.x.max;
		options2.vAxis.viewWindow.min = coords.y.min;
		options2.vAxis.viewWindow.max = coords.y.max;
		}
		chart2.draw(data2, options2);
		}
		},
		packages: ['corechart','annotatedtimeline']
		});
		
		
		google.charts.load('current', {'packages':['corechart']});
		google.charts.setOnLoadCallback(drawChart);
		function drawChart() 
		{var data = new google.visualization.DataTable();
		data.addColumn('datetime', 'Date');
		data.addColumn('number', 'value');
		data.addColumn({type: 'string', role:'annotation'});
		data.addColumn({type: 'string', role:'annotationText'});
		data.addColumn('number', 'movingAverage');
		data.addColumn('number', 'movingAverage2');
		data.addRows([""")
		