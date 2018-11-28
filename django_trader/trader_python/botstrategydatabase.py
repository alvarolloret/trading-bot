import sys
import getopt
from time import mktime as mktime
from datetime import datetime
from django.utils.timezone import utc
import time
from trader_app.models import CandleStick, Strategy
from trader_python.botcandlestick import BotCandlestick
from binance.client import Client
from django.core.serializers.json import DjangoJSONEncoder


class BotStrategyDatabase(object):
    def __init__(self, variables):
        self.vars = variables
        self.pair = self.vars.pair
        self.period = self.vars.period
        self.database = self.vars.database
        self.start=self.vars.startTime
        self.end=self.vars.endTime
        self.populateDatabase()
        self.updateDatabase();

    def retrieveValuesDatabase(self):
        # https://docs.djangoproject.com/en/2.1/ref/models/querysets/#range
        databasefiltered = eval(self.database).objects.filter(date__range=(self.start, self.end), pair__icontains=self.pair, period__icontains=self.period)
        data=[]
        for kline in databasefiltered:
            data.append(BotCandlestick(self.period, kline.open, kline.close, kline.high, kline.low, kline.average, kline.date)) #because in miliseconds
        return data

    def updateDatabase(self):


        # https://docs.djangoproject.com/en/2.1/ref/models/querysets/#latest
        latest=eval(self.database).objects.filter( pair__icontains=self.pair, period__icontains=self.period).latest('date') #This is the output: CandleStick_4H_ETH_USDT object (4236)
        # https://stackoverflow.com/a/5769695/5176549
        Date = latest.date # <class 'datetime.datetime'>: 2018-11-01 01:00:00+00:00
        # https://www.tutorialspoint.com/How-to-convert-Python-datetime-to-epoch-with-strftime
        timestamp=Date.timestamp() #<class 'float'>  1541034000.0
        print ("Updating database from: "+Date.strftime("%Y-%m-%d %H:%M"))
        self.startTime = str(timestamp)
        self.endTime = str(time.time()) #time now in timestamp
        self.loadValues()

    def populateDatabase(self):
        self.startTime = str(mktime(time.strptime(
            '2018-06-01', '%Y-%m-%d')))
        self.endTime = str(mktime(time.strptime(
            '2018-08-01', '%Y-%m-%d')))
        print ("Populating database from: "+self.startTime + " to: "+self.endTime)
        self.loadValues()


    def loadValues(self):
        client = Client("", "")
        klines = client.get_historical_klines(self.pair, getattr(
            client, self.period), self.start, self.end)
        for kline in klines:
            time1=int(kline[0]/1000)
            # create.arduino.cc/projecthub/feilipu/using-freertos-multi-tasking-in-arduino-ebc3cc
            t=datetime.fromtimestamp(time1).replace(tzinfo=utc)
            t=t.strftime('%Y-%m-%d %H:%M')

            # https://docs.djangoproject.com/en/2.1/topics/db/queries/
            p = eval(self.database)(pair=self.pair, period=self.period, date=t, high=float(kline[2]), low=float(kline[3]), open=float(kline[1]),close=float(kline[4]), average=((float(kline[1])+float(kline[2])+float(kline[4])+float(kline[3]))/4))
            p.save()

    # For seriqlizing datetime formats
    # https://stackoverflow.com/a/11875813/5176549
