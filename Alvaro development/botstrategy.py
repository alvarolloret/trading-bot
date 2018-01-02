from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade
from botvariables import botVariables
import datetime

class BotStrategy(object):
	#--------------------------------------------------------------#
	#---------Part 1.2: initialisating the bot strategy------------#
	#--------------------------------------------------------------#
	def __init__(self):
		self.vars=botVariables()
		self.investement=botVariables().showInvestment()
		self.makeFee=botVariables().showMakeFee()
		self.takeFee=botVariables().showTakeFee()
		self.output = BotLog()
		self.prices = []
		self.closes = [] # Needed for Momentum Indicator
		self.trades = []
		self.numOfTrades=0
		self.currentPrice = ""
		self.currentTime=""
		self.currentClose = ""
		self.numSimulTrades = 1
		self.indicators = BotIndicators()
		self.absMargin = 0
		self.relMargin = 0
	#--------------------------------------------------------------#
	#---END:--Part 1.2: initialisating the bot strategy------------#
	#--------------------------------------------------------------#
	
	
	
	
	
	
	
	#--------------------------------------------------------------#
	#---------Part 1.3: Evaluating each candlestic from the chart--#
	#--------------------------------------------------------------#
	#--------------------USING THE STRATEGY TICK-------------------#
	#--------------------------------------------------------------#
	def tick(self,candlestick): #where a candlestick is a an item of the list BotChart.getPoints
		self.currentPrice = float(candlestick.priceAverage)
		self.currentTime = candlestick.date
		self.prices.append(self.currentPrice)
		
		#self.currentClose = float(candlestick['close'])
		#self.closes.append(self.currentClose)
		
		#self.output.log(datetime.datetime.fromtimestamp(self.currentTime).strftime('%Y-%m-%d %H:%M:%S')+" - Price: "+str(candlestick.priceAverage)+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,self.vars.movingAvPeriod,self.currentPrice)))

		self.evaluatePositions(candlestick)
		self.updateOpenTrades(candlestick)
		self.showPositions()

		
		
	def evaluatePositions(self,candlestic):
		openTrades = []
		for trade in self.trades:
			if (trade.status == "OPEN"):
				openTrades.append(trade)
				
				
		
		if (len(openTrades) < self.numSimulTrades):
			#--------------------------------------------------------------#
			#------Part 1.3.A: Adding a trade if the conditions are met----#
			#--------------------------------------------------------------#
			SMA1=self.indicators.movingAverage(self.prices,self.vars.movingAvPeriod,self.currentPrice)
			SMA2=self.indicators.movingAverage(self.prices,self.vars.movingAvPeriod2,self.currentPrice)
			EMA1=self.indicators.EMA(self.prices,self.vars.movingAvPeriod,self.currentPrice)
			EMA2=self.indicators.EMA(self.prices,self.vars.movingAvPeriod2,self.currentPrice)
			if SMA2 < SMA1:
				#self.output.log("Trade Opened. Currentprice: "+str(self.currentPrice)+", MovAverage: "+str(self.indicators.movingAverage(self.prices,self.vars.movingAvPeriod,self.currentPrice)))
				candlestic.label="'Buy'"
				self.trades.append(BotTrade(self.currentTime,self.currentPrice))
				self.numOfTrades+=1
				

		for trade in openTrades:
			SMA1=self.indicators.movingAverage(self.prices,self.vars.movingAvPeriod,self.currentPrice)
			SMA2=self.indicators.movingAverage(self.prices,self.vars.movingAvPeriod2,self.currentPrice)
			EMA1=self.indicators.EMA(self.prices,self.vars.movingAvPeriod,self.currentPrice)
			EMA2=self.indicators.EMA(self.prices,self.vars.movingAvPeriod2,self.currentPrice)
			if SMA2 > SMA1:
				#self.output.log("Trade Closed. Currentprice: "+str(self.currentPrice)+", MovAverage: "+str(self.indicators.movingAverage(self.prices,self.vars.movingAvPeriod,self.currentPrice)))
				candlestic.label="'Sell'"
				trade.close(self.currentPrice, self.currentTime)

	
	def updateOpenTrades(self, candlestic):
		status=""
		for trade in self.trades:
			if (trade.status == "OPEN"):
				status+=trade.update(self.currentPrice, self.currentTime) #returns if state is open or close
				if status=="CLOSED":
					candlestic.label="'StopLoss'"
				

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()
			
	def showMargin(self):
		tradeStatus="Stat"
		for trade in self.trades:
			if (trade.status == "CLOSED"):
				tradeStatus=datetime.datetime.fromtimestamp(trade.exitTime).strftime('%Y-%m-%d %H:%M:%S')+" "+ str(trade.status) + " Entry: "+str(trade.entryPrice)+" Exit: "+str(trade.exitPrice)
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
				
		self.output.log(tradeStatus)
		
	def makeInvesment(self, trade):
		self.investement= ((1-self.makeFee)*self.investement/trade.entryPrice)*((1-self.takeFee)*trade.exitPrice)
		
		
	def showTrades(self):
		return self.trades