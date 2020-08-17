from django import forms
from .models import *
from bootstrap_datepicker_plus import DatePickerInput

class SearchForm(forms.Form):
    personnages = forms.ModelMultipleChoiceField(queryset=Personnage.objects.all(), required=False)
    categories = forms.ModelMultipleChoiceField(queryset=Categorie.objects.all(), required=False)
    combined = forms.BooleanField(required=False)
    date_depart = forms.DateField(required=True, initial=Evenement.objects.order_by('date').first().date, widget=DatePickerInput(format='%d/%m/%Y'))
    date_fin = forms.DateField(required=True, initial=Evenement.objects.order_by('date').last().date, widget=DatePickerInput(format='%d/%m/%Y'))
