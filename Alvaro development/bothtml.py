
class BotHTML(object):
	def __init__(self):

		self.begin="""<html><head><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>


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
				data.addRows(["""




		self.end="""]);
				var options = {title: 'Price Chart',
				hAxis:
					{format: 'MMM, dd, yyyy, HH:mm'},
				explorer:
					{actions: ['dragToZoom', 'rightClickToReset'],axis: 'horizontal',maxZoomIn: 100.0},
				legend:
					{ position: 'bottom' }};


				var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
				chart.draw(data, options);
				}

				</script></head>
				<body><div id="curve_chart" style="width: 100%; height: 70%"></div></body>
				</html>"""


		self.javascript="""<html><head><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>


			<script type="text/javascript">google.charts.load('current', {
			callback: function () {
			var chart1;
			var chart2;

			var data1 = new google.visualization.DataTable();
			var data2 = new google.visualization.DataTable();

			var container1 = document.getElementById('price-chart');
			var container2 = document.getElementById('rsi-chart');

			var outDiv1 = document.getElementById('price-chart-event');
			var outDiv2 = document.getElementById('rsi-chart-event');

			var options1 = {title:'Price Chart',
				height:500,
				displayAnnotations: false,
      	displayZoomButtons: false,
				chartArea: { width:'90%',height:'90%'},
				hAxis:
					{format: 'MMM, dd, yyyy, HH:mm'},
				explorer:
					{actions: ['dragToZoom', 'rightClickToReset'],axis: 'horizontal',maxZoomIn: 100.0},
				legend:
					{ position: 'bottom' },
			  crosshair: {
				trigger: 'both'
				//orientation: 'vertical'
			  }
			};

			var options2 = {
				height:100,
				chartArea: { width:'90%',height:'90%'},
				displayZoomButtons: false,
      	displayRangeSelector: false,
				vAxis: {
            viewWindowMode:'explicit',
            viewWindow: {
              max:100,
              min:0
            }},
				hAxis:
					{format: 'MMM, dd, yyyy, HH:mm'},
				explorer:
					{actions: ['dragToZoom', 'rightClickToReset'],axis: 'horizontal',maxZoomIn: 100.0},
				legend:
					{ position: 'bottom' },
			  crosshair: {
				trigger: 'both'
				//orientation: 'vertical'
			  }
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
			}"""

		self.chart11="""
			function drawChartOne(data) {
				data.addColumn('datetime', 'Date');
				data.addColumn('number', 'value');
				data.addColumn({type: 'string', role:'annotation'});
				data.addColumn({type: 'string', role:'annotationText'});
				data.addColumn('number', 'movingAverage');
				data.addColumn('number', 'movingAverage2');
				data.addRows(["""

		self.chart12="""])
			  chart1 = new google.visualization.LineChart(container1);
			}"""

		self.chart21="""
			function drawChartTwo(data) {
			  data.addColumn('datetime', 'Date');
			  data.addColumn('number', 'rsi');
				data.addRows(["""

		self.chart22="""])
			  chart2 = new google.visualization.LineChart(container2);
			}"""

		self.endjavascript="""
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
				options2.vAxis.viewWindow.min = 0;
				options2.vAxis.viewWindow.max = 100;
			  }
			  chart2.draw(data2, options2);
			}
		  },
		  packages: ['corechart','annotatedtimeline']
		});</script>
		<div id="price-chart"></div>
		<div id="rsi-chart"></div>
		<div id="price-chart-event"></div>
		<div id="rsi-chart-event"></div>"""
