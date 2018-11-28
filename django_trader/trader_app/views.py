from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from trader_app.models import User
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
from trader_python.botdatabase import BotDatabase
from colorama import init  # THis is only for color printing


#Importing stuff for logins
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from trader_app.forms import UserForm,UserProfileInfoForm
from django.shortcuts import redirect
from django.urls import reverse
from . import models
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView)


# For reading DateTimeField, see outputResult
# https://stackoverflow.com/a/27058505/5176549
import json
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

def index(request):
    return render(request, 'trader_app/index.html')

# def outputResult(request):
#     print ("hola?")
#     # https://stackoverflow.com/a/32787887/5176549
#     dataChartRetrieved=request.session.get('data')
#     return render(request, 'trader_app/outputResult.html', {'data':dataChartRetrieved})

class outputResult(ListView):
    # https://stackoverflow.com/a/33350839/5176549
    model = models.CandleStick
    # paginate_by = 10

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', 'give-default-value')
        order = self.request.GET.get('orderby', 'give-default-value')
        new_context = Update.objects.filter(
            state=filter_val,
        )
        return new_context

    def get_context_data(self, **kwargs):
        context = super(MyView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', 'give-default-value')
        context['orderby'] = self.request.GET.get('orderby', 'give-default-value')
        return context


def livetesting(request):
    return render(request, 'trader_app/livetesting.html')


def backtest(request):
    form = forms.FormBacktest()

    if request.method == 'POST':
        form = forms.FormBacktest(request.POST)
        if form.is_valid():
            print("VALIDATION SUCCESS!")
            print("Start: " + str(form.cleaned_data['dateStart']))
            print("End: " + str(form.cleaned_data['dateEnd']))
            print("Pair: " + str(form.cleaned_data['pairChosen']))
            print("Period: " + str(form.cleaned_data['periodChosen']))


            init()  # THis is only for color printing


            variables = botVariables()
            time1=form.cleaned_data['dateStart'].strftime('%Y-%m-%d %H:%M:%S')
            time2=form.cleaned_data['dateEnd'].strftime('%Y-%m-%d %H:%M:%S')
            pair=form.cleaned_data['pairChosen']
            period=form.cleaned_data['periodChosen']
            variables.modifyStartTime(time1)
            variables.modifyEndTime(time2)
            variables.modifyPair(pair)
            variables.modifyPeriod(period)



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


                database=BotDatabase(variables)
                data=database.retrieveValuesDatabase()


                strategy = BotStrategy()

                for candlestick in data:
                    strategy.tick(candlestick)
                    database.addStrategyCandlestick()

                strategy.showMargin()

                chart = BotChart(variables, data)
                dataChart=chart.returnData()
                data= json.dumps( dataChart, default=DateTimeEncoder)
                request.session['data'] = data


            else:
                print("TODO: Live trading")

            return  redirect('/trader_app/outputResult',   kwargs={ 'data': dataChart })
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
