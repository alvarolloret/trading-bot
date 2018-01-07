import numpy
from botvariables import botVariables

class BotIndicators(object):
	def __init__(self):
		self.vars=botVariables()
		pass

	def movingAverage(self, dataPoints, period,currentPrice):
		if (len(dataPoints) > 1):
			return sum(dataPoints[-period:]) / float(len(dataPoints[-period:]))
		else:
			return currentPrice

	def momentum (self, dataPoints, period=14):
		if (len(dataPoints) > period -1):
			return dataPoints[-1] * 100 / dataPoints[-period]

	def EMA(self, prices, period, currentPrice):
		if (len(prices) > 1):
			dataPrices = numpy.asarray(prices)
			weights = None
			weights = numpy.exp(numpy.linspace(-1., 0., period)) #if period=10: array([ 0.36787944,  0.41111229,  0.45942582,  0.51341712,  0.57375342, 0.64118039,  0.71653131,  0.8007374 ,  0.89483932,  1. ])
			weights /= weights.sum() #if period=10: array([ 0.03857234,  0.04142829,  0.0444957 ,  0.04779023,  0.05132868, 0.05512913,  0.05921097,  0.06359504,  0.0683037 ,  0.07336101, 0.07879276,  0.08462669,  0.09089257,  0.09762239,  0.10485049])

			a = numpy.convolve(dataPrices, weights, mode='full')[:len(dataPrices)]
			return a[-1]
		else:
			return currentPrice

	def MACD(self, prices, nslow=26, nfast=12):
		emaslow = self.EMA(prices, nslow)
		emafast = self.EMA(prices, nfast)
		return emaslow, emafast, emafast - emaslow

	def RSI (self, prices):
		period=float(self.vars.RSIPeriod)
		deltas = numpy.diff(prices)
		seed = deltas[:int(period)+1]
		up = seed[seed >= 0].sum()/period
		down = -seed[seed < 0].sum()/period
		rs = up/down
		rsi = numpy.zeros_like(prices)
		rsi[:int(period)] = 100. - 100./(1. + rs)

		for i in range(int(period), len(prices)):
 			delta = deltas[i - 1]  # cause the diff is 1 shorter
  			if delta > 0:
 				upval = delta
 				downval = 0.
 			else:
 				upval = 0.
 				downval = -delta

 			up = (up*(period - 1) + upval)/period
 			down = (down*(period - 1) + downval)/period
  			rs = up/down
 			rsi[i] = 100. - 100./(1. + rs)
  		if len(prices) > period:
 			return rsi[-1]
 		else:
 			return 50 # output a neutral amount until enough prices in list to calculate RSI

	def BollUp(self, dataPoints, period,currentPrice):
		if (len(dataPoints) > 1):
			movAv=sum(dataPoints[-period:]) / float(len(dataPoints[-period:]))
			strandarDeviation=numpy.std(dataPoints[-period:])
			return movAv+strandarDeviation*self.vars.BollNumOfStd
		else:
			return currentPrice

	def BollDown(self, dataPoints, period,currentPrice):
		if (len(dataPoints) > 1):
			movAv=sum(dataPoints[-period:]) / float(len(dataPoints[-period:]))
			strandarDeviation=numpy.std(dataPoints[-period:])
			return movAv-strandarDeviation*self.vars.BollNumOfStd
		else:
			return currentPrice
