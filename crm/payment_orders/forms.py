from django import forms

from .models import PaymentOrder


class PaymentOrderForm(forms.ModelForm):
    class Meta:
        model = PaymentOrder
        fields = [
            'number',
            'date',
            'payment_kind',
            'organization',
            'recipient',
            'amount',
            'amount_text',
            'payment_purpose',
            'kbk',
            'oktmo',
            'payment_operation_type',
            'payment_due_date',
            'payment_assignment_code',
            'payment_priority',
            'payment_code',
            'reserve_field',
            'payment_basis',
            'tax_period',
            'doc_number',
            'doc_date',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'doc_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_purpose': forms.Textarea(attrs={'rows': 3}),
        }
