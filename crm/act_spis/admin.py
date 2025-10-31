from django.contrib import admin

from .models import ActSpis, ActSpisItem


class ActSpisItemInline(admin.TabularInline):
	model = ActSpisItem
	extra = 0


@admin.register(ActSpis)
class ActSpisAdmin(admin.ModelAdmin):
	list_display = ('id', 'date', 'customer', 'contract', 'invoice', 'delivery_method', 'warehouse')
	list_filter = ('date', 'customer')
	search_fields = ('id', 'contract', 'invoice', 'warehouse')
	inlines = [ActSpisItemInline]
