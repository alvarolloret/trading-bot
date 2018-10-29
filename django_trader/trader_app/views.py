from django.shortcuts import render
from django.http import HttpResponse
from trader_app.models import User, CandleStick
from . import forms

# Importing main from python trader.
import sys
import getopt
import time
from trader_python.botvariables import botVariables
from trader_python.botchart import BotChart
from trader_python.botstrategy import BotStrategy
from trader_python.botlog import BotLog
from trader_python.botcandlestick import BotCandlestick
from colorama import init  # THis is only for color printing


def index(request):
    form = forms.FormBacktest()

    if request.method == 'POST':
        form = forms.FormBacktest(request.POST)
        if form.is_valid():
            # DO SOMETHING CODE
            print("VALIDATION SUCCESS!")
            print("Start: " + str(form.cleaned_data['dateStart']))
            print("Start: " + str(form.cleaned_data['dateEnd']))

            init()  # THis is only for color printing
            variables = botVariables()
            startTime = True
            endTime = False

            if (startTime):

                #--------------------------------------------------------------#
                #---------Part 1.1: picking up the data from the market--------#
                #--------------------------------------------------------------#
                print(("PAIR: " + str(variables.pair) +
                       ", period: " + str(variables.period)))

                chart = BotChart(variables.market, variables.pair,
                                 variables.period, variables.startTime, variables.endTime)

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
                chart.creatChartRSI()
                # chart.createChart()
            #---------------END: Part 1: Backtesting--------------------#

            else:
                print("TODO: Live trading")


    return render(request, 'trader_app/index.html', {'form': form})
