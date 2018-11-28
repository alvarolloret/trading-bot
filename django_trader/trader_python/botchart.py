#from exchange import poloniex
from trader_python import poloniex
import urllib.request
import urllib.parse
import urllib.error
import json
import pprint
import datetime
from trader_python.botdatabase import BotDatabase
from trader_python.botcandlestick import BotCandlestick
from trader_python.botindicators import BotIndicators
from trader_python.bottrade import BotTrade
from trader_python.bothtml import BotHTML
from binance.client import Client


class BotChart(object):

    def __init__(self, variables, data):
        self.botHTML = BotHTML()
        self.vars = variables
        self.avPeriod = self.vars.movingAvPeriod
        self.indicators = BotIndicators()
        self.pair = self.vars.pair
        self.period = self.vars.period
        self.startTime = self.vars.startTime
        self.endTime = self.vars.endTime
        self.data = data
        self.prices = []
        self.trades = []


    def returnData(self):
        historicalData = self.data
        dataPoints = []
        priceData = []
        label = 'null'
        data = []

        while True:
            # step 0: iterating over data points
            if (self.startTime and historicalData):
                # https://stackoverflow.com/a/4426727/5176549
                nextDataPoint = historicalData.pop(0)
                lastPairPrice = nextDataPoint.priceAverage
                priceData.append(float(lastPairPrice))
                movingAverage = self.indicators.movingAverage(
                    priceData, self.vars.movingAvPeriod, lastPairPrice)
                movingAverage2 = self.indicators.movingAverage(
                    priceData, self.vars.movingAvPeriod2, lastPairPrice)
                label = nextDataPoint.label
                dataDate = nextDataPoint.date
                # adding the trades on the label

            # step 2: once the iteration is finished, adding all the info in the chart
            elif(self.startTime and not historicalData):
                print("Finished")
                # for point in dataPoints:
                #     data.append([point['date'], point['price'],
                #                  point['label'], point['desc'], point['movAv1'], point['movAv2']])

                break

            # step 1: addind the last point on the list
            else:
                currentValues = conn.api_query("returnTicker")
                lastPairPrice = currentValues[pair]["last"]
                dataDate = datetime.datetime.now()

            # Main step: appending values to local dataPoints
            dataPoints.append({
                'date': dataDate,
                'price': lastPairPrice,
                'movAv1': movingAverage,
                'movAv2': movingAverage2,
                'label': label,
                'desc': 'null'})
        return dataPoints

    def stringToDate(self, date):
        # date is the follwing format: date='2017-12-27 11:50:00'
        return "new Date(" + date[0:4] + ", " + date[5:7] + ", " + date[8:10] + ", " + date[11:13] + ", " + date[14:16] + ")"
        # "new Date(%d,%d,%d,%d,%d,%d,%d)" (int(date[0:4]),int(date[5:7]),int(date[8:10]),int(date[11:13]),int(date[14:16]))

    def getPoints(self):
        return self.data

    def getCurrentPrice(self):
        currentValues = self.conn.api_query("returnTicker")
        lastPairPrice = {}
        lastPairPrice = currentValues[self.pair]["last"]
        return lastPairPrice

    def getLastPrices(self, date, dataCandlestick, period):
        lastPrices = []
        # https://stackoverflow.com/a/3940144/5176549
        for candlestick in reversed(dataCandlestick):
            lastPrices.append(candlestick['weightedAverage'])
            if date == (candlestick['date']):
                break
        return lastPrices[-period:]

    def createChart(self):
        historicalData = self.data
        dataPoints = []
        priceData = []
        label = 'null'
        output = open("output.html", 'w')
        output.truncate()
        # Understanding googlechart: https://developers.google.com/chart/interactive/docs/basic_load_libs
        output.write(self.botHTML.begin)

        while True:

            # step 0: iterating over data points
            if (self.startTime and historicalData):
                # https://stackoverflow.com/a/4426727/5176549
                nextDataPoint = historicalData.pop(0)
                lastPairPrice = nextDataPoint.priceAverage
                priceData.append(float(lastPairPrice))
                movingAverage = self.indicators.movingAverage(
                    priceData, self.vars.movingAvPeriod, lastPairPrice)
                movingAverage2 = self.indicators.movingAverage(
                    priceData, self.vars.movingAvPeriod2, lastPairPrice)
                label = nextDataPoint.label
                dataDate = nextDataPoint.date
                # adding the trades on the label

            # step 2: once the iteration is finished, adding all the info in the chart
            elif(self.startTime and not historicalData):
                print("Finished Writing data on chart")

                for point in dataPoints:
                    output.write("[" + self.stringToDate(point['date']) + "," + point['price'] + "," +
                                 point['label'] + "," + point['desc'] + "," + point['movAv1'] + "," + point['movAv2'])
                    output.write("],\n")
                output.write(self.botHTML.end)
                break

            # step 1: addind the last point on the list
            else:
                currentValues = conn.api_query("returnTicker")
                lastPairPrice = currentValues[pair]["last"]
                dataDate = datetime.datetime.now()

            # Main step: appending values to local dataPoints
            dataPoints.append({
                'date': dataDate,
                'price': str(lastPairPrice),
                'movAv1': str(movingAverage),
                'movAv2': str(movingAverage2),
                'label': label,
                'desc': 'null'})

    def creatChartRSI(self):
        # Double Chart zoom: https://stackoverflow.com/a/42238747/5176549 or https://jsfiddle.net/pzamu7kt/
        # Understanding googlechart: https://developers.google.com/chart/interactive/docs/basic_load_libs
        historicalData = self.data
        dataPoints = []
        priceData = []
        movingAverage = 0
        label = 'null'
        output = open("outputrsi.html", 'w')
        output.truncate()
        # Understanding googlechart: https://developers.google.com/chart/interactive/docs/basic_load_libs
        output.write(self.botHTML.javascript)

        while True:
            # step 0: iterating over data points
            if (self.startTime and historicalData):
                nextDataPoint = historicalData.pop(0)
                # https://stackoverflow.com/a/4426727/5176549
                lastPairPrice = nextDataPoint.priceAverage
                priceData.append(float(lastPairPrice))
                BollUp = self.indicators.BollUp(
                    priceData, self.vars.BollPeriod, lastPairPrice)
                BollDown = self.indicators.BollDown(
                    priceData, self.vars.BollPeriod, lastPairPrice)
                rsiData = self.indicators.RSI(priceData)
                label = nextDataPoint.label
                dataDate = datetime.datetime.fromtimestamp(
                    int(nextDataPoint.date)).strftime('%Y-%m-%d %H:%M:%S')
                # adding the trades on the label

            # step 2: once the iteration is finished, adding all the info in the chart
            elif(self.startTime and not historicalData):
                output.write(self.botHTML.chart11)
                for point in dataPoints:
                    output.write("[" + self.stringToDate(point['date']) + "," + point['price'] + "," +
                                 point['label'] + "," + point['desc'] + "," + point['BollUp'] + "," + point['BollDown'])
                    output.write("],\n")
                output.write(self.botHTML.chart12)
                output.write(self.botHTML.chart21)
                for point in dataPoints:
                    # print (point['rsi'])
                    output.write(
                        "[" + self.stringToDate(point['date']) + "," + point['rsi'])
                    output.write("],\n")
                output.write(self.botHTML.chart22)
                output.write(self.botHTML.endjavascript)
                break

            # step 1: addind the last point on the list
            else:
                currentValues = conn.api_query("returnTicker")
                lastPairPrice = currentValues[pair]["last"]
                dataDate = datetime.datetime.now()

            # Main step: appending values to local dataPoints
            dataPoints.append({
                'date': dataDate,
                'price': str(lastPairPrice),
                'BollUp': str(BollUp),
                'BollDown': str(BollDown),

                'rsi': str(rsiData),
                'label': label,
                'desc': 'null'})
