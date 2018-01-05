import sys, getopt

class botVariables(object):
	def __init__(self):
		self.pair="USDT_BTC"
		self.period=300

		self.movingAvPeriod = 5
		self.movingAvPeriod2 = 20
		self.RSIPeriod = 14

		self.initialInvestment = 100 #in euros

		self.stopLoss=500 #in the pair, for examle BTC_USD

		self.makeFee=0.0005 #0.1% of the buying fees
		self.takeFee=0.0005 #0.1% of the selling fees

		self.api_key='RZPH057A-1L01XZUI-TL2ZCFLP-0QK92K9J'
		self.api_secret='f50a8cd597bca93d33e997603b754277ac7e7e98e4ed4da37470f7d184639af089278633bbe9aac3e54da0042673823fcd3d8a5c34112396b4a158a9203ab698'

	#Showning variables
	#Check this anwer https://stackoverflow.com/a/32802486/5176549
	def showPeriod(self):
		return self.period

	def showMovAvPeriod(self):
		return self.movingAvPeriod

	def showInvestment(self):
		return self.initialInvestment

	def showMovAvPeriod(self):
		return self.movingAvPeriod

	def showMakeFee(self):
		return self.makeFee

	def showTakeFee(self):
		return self.takeFee

	def showApiKey(self):
		return self.api_key

	def showApiSecret(self):
		return self.api_secret

	def modifyInvestement(self, value):
		self.initialInvestment=value
		return self.initialInvestment
