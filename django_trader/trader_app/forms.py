from django import forms
# from django.forms import extras
from django.forms.widgets import *
from django.core import validators
from bootstrap3_datetime.widgets import DateTimePicker
import datetime

from django.contrib.auth.models import User
from trader_app.models import UserProfileInfo

Pair_CHOICES= [
    ('ETHUSDT', 'USDT_ETH'),
    ('others', 'Others'),
    ]
Period_CHOICES= [
        ('KLINE_INTERVAL_4HOUR', '4h'),
        ('others', 'Others'),
        ]

class FormBacktest(forms.Form):
    class Meta:  #https://stackoverflow.com/a/41530469/5176549
        fields = ['completeDateTime']
        widgets = {
            'completeDateTime': forms.DateTimeInput(attrs={'class': 'datetime-input'})
        }

    dateStart = forms.DateTimeField(required=False, widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm"}))
    dateEnd = forms.DateTimeField(required=False, widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm"}))

    # http://www.learningaboutelectronics.com/Articles/How-to-create-a-drop-down-list-in-a-Django-form.php
    pairChosen= forms.CharField(label='Pair', widget=forms.Select(choices=Pair_CHOICES))
    periodChosen= forms.CharField(label='Period', widget=forms.Select(choices=Period_CHOICES))


    def clean(self):
        all_clean_data = super().clean()
        start = all_clean_data['dateStart']
        end = all_clean_data['dateEnd']
        pair = all_clean_data['pairChosen']
        period = all_clean_data['periodChosen']
        print (pair)
        if start is None:
            raise forms.ValidationError("Start is empty")
        elif end is None:
            raise forms.ValidationError("End is empty")
        elif (start > end):
            raise forms.ValidationError("Start is later than end")
        elif (pair == "others" or period == "others"):
            raise forms.ValidationError("Others are still in development")


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')
