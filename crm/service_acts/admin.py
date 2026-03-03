from django.contrib import admin

from .models import ServiceAct, ServiceActLine


class ServiceActLineInline(admin.TabularInline):
    model = ServiceActLine
    extra = 0


@admin.register(ServiceAct)
class ServiceActAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'executor', 'customer', 'total_without_vat')
    list_filter = ('executor', 'customer')
    search_fields = ('number', 'executor__name', 'customer__name')
    inlines = [ServiceActLineInline]


@admin.register(ServiceActLine)
class ServiceActLineAdmin(admin.ModelAdmin):
    list_display = ('act', 'order', 'name', 'quantity', 'price', 'vat_rate', 'amount_without_vat', 'vat_amount', 'amount_with_vat')
    list_filter = ('act',)
    search_fields = ('name',)
