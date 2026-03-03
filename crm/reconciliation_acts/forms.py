from django import forms
from django.forms import inlineformset_factory

from .models import ReconciliationAct, ReconciliationActLine


class ReconciliationActForm(forms.ModelForm):
    class Meta:
        model = ReconciliationAct
        fields = [
            'number',
            'date',
            'organization',
            'customer',
            'period_from',
            'period_to',
            'opening_balance',
            'closing_balance',
            'opening_balance_customer',
            'closing_balance_customer',
            'note',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'period_from': forms.DateInput(attrs={'type': 'date'}),
            'period_to': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }


class ReconciliationActLineForm(forms.ModelForm):
    class Meta:
        model = ReconciliationActLine
        fields = [
            'order',
            'date',
            'document',
            'debit',
            'credit',
            'customer_debit',
            'customer_credit',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


ReconciliationActLineFormSet = inlineformset_factory(
    ReconciliationAct,
    ReconciliationActLine,
    form=ReconciliationActLineForm,
    fields=[
        'order',
        'date',
        'document',
        'debit',
        'credit',
        'customer_debit',
        'customer_credit',
    ],
        extra=0,
    can_delete=True,
)
