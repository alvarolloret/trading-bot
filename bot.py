import sys, getopt
import time

from botvariables import botVariables
from botchart import BotChart
from botstrategy import BotStrategy
from botlog import BotLog
from botcandlestick import BotCandlestick

from colorama import init  #THis is only for color printing

def main(argv):
	init()  #THis is only for color printing
	variables=botVariables()
	startTime = True
	endTime = False


	#-----------------------------------------------------------------#
	#-------------------Part 0: Passing arguments---------------------#
	#-----------------------------------------------------------------#
	# try:
	# 	opts, args = getopt.getopt(argv,"hp:c:n:s:e:",["period=","currency=","points="])
	# except getopt.GetoptError:
	# 	print 'trading-bot.py -p <period length> -c <currency pair> -n <period of moving average>'
	# 	sys.exit(2)
    #
	# for opt, arg in opts:
	# 	if opt == '-h':
	# 		print 'trading-bot.py -p <period length> -c <currency pair> -n <period of moving average>'
	# 		sys.exit()
	# 	elif opt in ("-p", "--period"):
	# 		if (int(arg) in [300,900,1800,7200,14400,86400]):
	# 			period = arg
	# 		else:
	# 			print 'Poloniex requires periods in 300,900,1800,7200,14400, or 86400 second increments'
	# 			sys.exit(2)
	# 	elif opt in ("-c", "--currency"):
	# 		pair = arg
	# 	elif opt in ("-n", "--points"):
	# 		lengthOfMA = int(arg)
	# 	elif opt in ("-s"):
	# 		startTime = arg
	# 	elif opt in ("-e"):
	# 		endTime = arg
    #
	#---------------END: Part 0: Passing arguments---------------------#






	#-----------------------------------------------------------------#
	#-------------------Part 1: Backtesting---------------------------#
	#-----------------------------------------------------------------#
	if (startTime):

		#--------------------------------------------------------------#
		#---------Part 1.1: picking up the data from the market--------#
		#--------------------------------------------------------------#
		print(("PAIR: "+str(variables.pair) + ", period: " + str(variables.period)))

		chart = BotChart("poloniex",variables.pair, variables.period, variables.startTime, variables.endTime)


		#--------------------------------------------------------------#
		#---------Part 1.2: initialisating the bot strategy------------#
		#--------------------------------------------------------------#
		strategy = BotStrategy()




		#--------------------------------------------------------------#
		#---------Part 1.3: Evaluating each candlestic from the chart--#
		#--------------------------------------------------------------#
		#--------------------USING THE STRATEGY TICK-------------------#
		#--------------------------------------------------------------#
		for candlestick in chart.getPoints():
			strategy.tick(candlestick)





		strategy.showMargin()
		#chart.creatChartRSI()
		chart.createChart()
	#---------------END: Part 1: Backtesting--------------------#




	else:
		print("TODO: Live trading")
		# chart = BotChart("poloniex",pair, period, startTime, endTime, False)
        #
		# strategy = BotStrategy()
        #
		# candlesticks = []
		# developingCandlestick = BotCandlestick()
        #
		# while True:
		# 	try:
		# 		developingCandlestick.tick(chart.getCurrentPrice())
		# 	except urllib2.URLError:
		# 		time.sleep(int(30))
		# 		developingCandlestick.tick(chart.getCurrentPrice())
        #
		# 	if (developingCandlestick.isClosed()):
		# 		candlesticks.append(developingCandlestick)
		# 		strategy.tick(developingCandlestick)
		# 		developingCandlestick = BotCandlestick()
        #
		# 	time.sleep(int(30))

if __name__ == "__main__":
	main(sys.argv[1:])
