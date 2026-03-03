from django import forms
from django.forms import inlineformset_factory

from .models import ServiceAct, ServiceActLine


class ServiceActForm(forms.ModelForm):
    class Meta:
        model = ServiceAct
        fields = ['number', 'date', 'executor', 'customer', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }


class ServiceActLineForm(forms.ModelForm):
    class Meta:
        model = ServiceActLine
        fields = ['order', 'name', 'unit', 'quantity', 'price', 'vat_rate']
        widgets = {
            'quantity': forms.NumberInput(attrs={'step': '0.001'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'vat_rate': forms.NumberInput(attrs={'step': '0.01'}),
        }


ServiceActLineFormSet = inlineformset_factory(
    ServiceAct,
    ServiceActLine,
    form=ServiceActLineForm,
    fields=['order', 'name', 'unit', 'quantity', 'price', 'vat_rate'],
    extra=1,
    can_delete=True,
)
