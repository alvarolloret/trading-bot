from django.shortcuts import render
from django.http import HttpResponse
from trader_app.models import User,CandleStick
from . import forms

# Create your views here.


def index(request):
    form = forms.FormBacktest()

    if request.method == 'POST':
        form = forms.FormBacktest(request.POST)
        if form.is_valid():
            # DO SOMETHING CODE
            print("VALIDATION SUCCESS!")
            print("Start: "+form.cleaned_data['dateStart'])
            print("Start: "+form.cleaned_data['dateEnd'])

    my_dict = {'insert_me':"Now I am coming from first_app/index.html!"}
    return render(request,'trader_app/index.html',context=my_dict)
