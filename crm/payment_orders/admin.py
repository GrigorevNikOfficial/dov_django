from django.contrib import admin

from .models import PaymentOrder


@admin.register(PaymentOrder)
class PaymentOrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'organization', 'recipient', 'amount')
    list_filter = ('date', 'organization')
    search_fields = ('number', 'organization__name', 'recipient__name')
