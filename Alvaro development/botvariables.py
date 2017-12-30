import sys, getopt

class botVariables(object):
	def __init__(self):
		self.movingAvPeriod = 11
		self.initialInvestment = 100 #in euros
		self.makeFee=0.0015 #0.15% of the buying fees
		self.takeFee=0.0025 #0.25% of the buying fees
		
	#Showning variables
	#Check this anwer https://stackoverflow.com/a/32802486/5176549
	def showInvestment(self):
		return self.initialInvestment
		
	def showMovAvPeriod(self):
		return self.movingAvPeriod
		
	def showMakeFee(self):
		return self.makeFee
		
	def showTakeFee(self):
		return self.takeFee

	def modifyInvestement(self, value):
		self.initialInvestment=value
		return self.initialInvestment