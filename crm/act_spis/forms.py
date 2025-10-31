from django import forms
from django.forms import inlineformset_factory

from .models import ActSpis, ActSpisItem


class ActSpisForm(forms.ModelForm):
    class Meta:
        model = ActSpis
        fields = ['date', 'customer', 'contract', 'warehouse', 'chairperson']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'contract': forms.TextInput(attrs={'maxlength': 255}),
            'warehouse': forms.TextInput(attrs={'maxlength': 255}),
            # chairperson is a select; widget left default
        }


class ActSpisItemForm(forms.ModelForm):
    class Meta:
        model = ActSpisItem
        fields = ['product', 'quantity', 'price']
        widgets = {
            'quantity': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }


ActSpisItemFormSet = inlineformset_factory(
    ActSpis,
    ActSpisItem,
    form=ActSpisItemForm,
    extra=1,
    can_delete=True,
)
