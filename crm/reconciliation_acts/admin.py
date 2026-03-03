from django.contrib import admin

from .models import ReconciliationAct, ReconciliationActLine


class ReconciliationActLineInline(admin.TabularInline):
    model = ReconciliationActLine
    extra = 0


@admin.register(ReconciliationAct)
class ReconciliationActAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'date',
        'organization',
        'customer',
        'period_from',
        'period_to',
        'closing_balance',
    )
    inlines = [ReconciliationActLineInline]


@admin.register(ReconciliationActLine)
class ReconciliationActLineAdmin(admin.ModelAdmin):
    list_display = (
        'act',
        'order',
        'date',
        'document',
        'debit',
        'credit',
        'customer_debit',
        'customer_credit',
    )
    list_filter = ('act',)
