from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from trader_app.models import User, CandleStick
from datetime import datetime
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


#Importing stuff for logins
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from trader_app.forms import UserForm,UserProfileInfoForm
from django.urls import reverse


def index(request):
    return render(request, 'trader_app/index.html')

def outputResult(request):
    return render(request, 'trader_app/outputResult.html')


def livetesting(request):
    print ("hola?")
    return render(request, 'trader_app/livetesting.html')


def backtest(request):
    form = forms.FormBacktest()

    if request.method == 'POST':
        form = forms.FormBacktest(request.POST)
        if form.is_valid():
            # DO SOMETHING CODE
            print("VALIDATION SUCCESS!")
            print("Start: " + str(form.cleaned_data['dateStart']))
            print("End: " + str(form.cleaned_data['dateEnd']))


            init()  # THis is only for color printing


            variables = botVariables()
            time1=form.cleaned_data['dateStart'].strftime('%Y-%m-%d %H:%M:%S')
            time2=form.cleaned_data['dateEnd'].strftime('%Y-%m-%d %H:%M:%S')
            variables.modifyStartTime(time1)
            variables.modifyEndTime(time2)



            startTime = True
            endTime = False

            if (startTime):

                #--------------------------------------------------------------#
                #---------Part 1.1: picking up the data from the market--------#
                #--------------------------------------------------------------#
                print(("PAIR: " + str(variables.pair) +
                       ", period: " + str(variables.period)))
                print(("Start: " + str(variables.startTime) +
                       ", End: " + str(variables.endTime)))
                chart = BotChart(variables)

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
                # dataChart=chart.returnData()
                dataChart=[]
                chart.createChart()

            #---------------END: Part 1: Backtesting--------------------#

            else:
                print("TODO: Live trading")


            return render(request, 'trader_app/outputResult.html', {'data': dataChart})
    return render(request, 'trader_app/backtest.html', {'form':form})


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'trader_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'trader_app/login.html', {})
