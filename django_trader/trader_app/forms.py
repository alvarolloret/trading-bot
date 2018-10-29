from django import forms
# from django.forms import extras
from django.forms.widgets import *
from django.core import validators
import datetime

class FormBacktest(forms.Form):
    dateStart = forms.DateField(widget=SelectDateWidget(years=[y for y in range(2016,2018)]))
    dateEnd= forms.DateField(widget=SelectDateWidget(years=[y for y in range(2016,2018)]))


    def clean(self):
        all_clean_data = super().clean()
        start = all_clean_data['dateStart']
        end = all_clean_data['dateEnd']

        if start > end:
            raise forms.ValidationError("Start is later than end")
