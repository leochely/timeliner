from django import forms
from .models import *
from bootstrap_datepicker_plus import DatePickerInput

class SearchForm(forms.Form):
    personnages = forms.ModelMultipleChoiceField(queryset=Personnage.objects.all())
    combined = forms.BooleanField(required=False)
    date_depart = forms.DateField(required=True, widget=DatePickerInput())
    date_fin = forms.DateField(required=True, widget=DatePickerInput())
