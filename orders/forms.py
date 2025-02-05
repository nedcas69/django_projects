from django import forms
from .models import Food, Table


class OrderForm(forms.Form):
    table = forms.ModelChoiceField(queryset=Table.objects.all(), label='Номер стола')
    items = forms.ModelMultipleChoiceField(
        queryset=Food.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Блюда'
    )
