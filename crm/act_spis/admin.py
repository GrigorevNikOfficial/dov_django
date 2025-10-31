from django.contrib import admin

from .models import ActSpis, ActSpisItem


class ActSpisItemInline(admin.TabularInline):
	model = ActSpisItem
	extra = 0


@admin.register(ActSpis)
class ActSpisAdmin(admin.ModelAdmin):
	def chairperson_position(self, obj):
		return obj.chairperson.position.name if obj.chairperson and obj.chairperson.position else ''
	chairperson_position.short_description = 'Должность'

	list_display = (
		'id',
		'date',
		'customer',
		'contract',
		'warehouse',
		'chairperson_position',
	)
	list_filter = ('date', 'customer')
	search_fields = ('id', 'contract', 'warehouse')
	inlines = [ActSpisItemInline]
