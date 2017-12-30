from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade
from botvariables import botVariables
import datetime

class BotStrategy(object):
	def __init__(self):
		self.investement=botVariables().showInvestment()
		self.makeFee=botVariables().showMakeFee()
		self.takeFee=botVariables().showTakeFee()
		self.output = BotLog()
		self.prices = []
		self.closes = [] # Needed for Momentum Indicator
		self.trades = []
		self.currentPrice = ""
		self.currentTime=""
		self.currentClose = ""
		self.numSimulTrades = 1
		self.indicators = BotIndicators()
		self.absMargin = 0
		self.relMargin = 0

	def tick(self,candlestick): #where a candlestick is a an item of the list BotChart.getPoints
		self.currentPrice = float(candlestick.priceAverage)
		self.currentTime = candlestick.date
		self.prices.append(self.currentPrice)
		
		#self.currentClose = float(candlestick['close'])
		#self.closes.append(self.currentClose)
		
		#self.output.log("Price: "+str(candlestick.priceAverage)+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,15)))

		self.evaluatePositions()
		self.updateOpenTrades()
		self.showPositions()

	def evaluatePositions(self):
		openTrades = []
		for trade in self.trades:
			if (trade.status == "OPEN"):
				openTrades.append(trade)

		if (len(openTrades) < self.numSimulTrades):
			if (self.currentPrice < self.indicators.movingAverage(self.prices,15,self.currentPrice)):
				self.trades.append(BotTrade(self.currentTime,self.currentPrice,stopLoss=.0001))
				

		for trade in openTrades:
			if (self.currentPrice*0.9975> self.indicators.movingAverage(self.prices,15,self.currentPrice)):
				trade.close(self.currentPrice)

	def updateOpenTrades(self):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.currentPrice)

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()
			
	def showMargin(self):
		for trade in self.trades:
			tradeStatus=datetime.datetime.fromtimestamp(trade.time).strftime('%Y-%m-%d %H:%M:%S')+" "+ str(trade.status) + " Entry: "+str(trade.entryPrice)+" Exit: "+str(trade.exitPrice)
			if (trade.status == "CLOSED"):
				self.makeInvesment(trade) #considering the trade as an indicator
				tradeStatus = tradeStatus + " Profit: "
				if (trade.exitPrice > trade.entryPrice):
					tradeStatus = tradeStatus + "\033[92m"
				else:
					tradeStatus = tradeStatus + "\033[91m"	
				tradeStatus = tradeStatus+str(trade.exitPrice - trade.entryPrice)+"\033[0m" + " Inves: "
				
				
				if (self.investement > botVariables().showInvestment()):
					tradeStatus = tradeStatus + "\033[92m"
				else:	
					tradeStatus = tradeStatus + "\033[91m"
				
				tradeStatus= tradeStatus+ str(self.investement)+"\033[0m"
				self.output.log(tradeStatus)
			
		#self.output.log(tradeStatus)
		
	def makeInvesment(self, trade):
		self.investement= ((1-self.makeFee)*self.investement/trade.entryPrice)*((1-self.takeFee)*trade.exitPrice)
		
	def showRelativeMargin(self):
		return (self.investement)/(botVariables().showInvesment())