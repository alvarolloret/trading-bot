from django import forms
# from django.forms import extras
from django.forms.widgets import *
from django.core import validators
from bootstrap3_datetime.widgets import DateTimePicker
import datetime


class FormBacktest(forms.Form):
    class Meta:  #https://stackoverflow.com/a/41530469/5176549
        fields = ['completeDateTime']
        widgets = {
            'completeDateTime': forms.DateTimeInput(attrs={'class': 'datetime-input'})
        }

    dateStart = forms.DateTimeField(required=False, widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm"}))
    dateEnd = forms.DateTimeField(required=False, widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm"}))
    def clean(self):
        all_clean_data = super().clean()
        start = all_clean_data['dateStart']
        end = all_clean_data['dateEnd']
        if start > end:
            raise forms.ValidationError("Start is later than end")
        
