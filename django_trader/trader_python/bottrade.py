from trader_python.botlog import BotLog
import datetime
from trader_python.botvariables import botVariables

class BotTrade(object):
	def __init__(self,time,currentPrice):
		self.output = BotLog()
		self.vars=botVariables()
		self.status = "OPEN"
		self.entryTime=time
		self.entryPrice = currentPrice
		self.exitTime = ''
		self.exitPrice = ""
		#self.output.log("Trade opened")
		if (self.vars.stopLoss>0):
			self.stopLoss = currentPrice - self.vars.stopLoss



	def close(self,currentPrice,currentTime):
		self.status = "CLOSED"
		self.exitPrice = currentPrice
		self.exitTime=currentTime
		#self.output.log("Trade closed")



	def update(self, currentPrice,currentTime):
		if (self.vars.stopLoss>0):
			if (currentPrice < self.stopLoss):
				self.close(currentPrice, currentTime)

		return self.status

	def showTrade(self):
		tradeStatus=""
		if (self.status == "CLOSED"):
			tradeStatus += datetime.datetime.fromtimestamp(self.exitTime).strftime('%Y-%m-%d %H:%M:%S')+" "+ str(self.status) + " Entry: "+str(self.entryPrice)+" Exit: "+str(self.exitPrice)
			tradeStatus = tradeStatus + " Profit: "
			if (self.exitPrice > self.entryPrice):
				tradeStatus = tradeStatus + "\033[92m"
			else:
				tradeStatus = tradeStatus + "\033[91m"

			tradeStatus = tradeStatus+str(self.exitPrice - self.entryPrice)+"\033[0m"

		#self.output.log(tradeStatus)

	def showTime(self):
		return self.entryTime

	def showEntryPrice(self):
		return self.EntryPrice
