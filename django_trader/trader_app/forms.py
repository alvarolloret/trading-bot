from django import forms
from django.core import validators
import datetime

class FormBacktest(forms.Form):
    dateStart = models.DateField(_("Start Date"), default=datetime.date.today)
    dateEnd = models.DateField(_("End Date"), default=datetime.date.today)


    def clean(self):
        all_clean_data = super().clean()
        start = all_clean_data['dateStart']
        end = all_clean_data['dateEnd']

        if start < end:
            raise forms.ValidationError("Start is later than end")
