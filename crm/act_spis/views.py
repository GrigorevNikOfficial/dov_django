from decimal import Decimal

import json

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import DecimalField, Sum, Value
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ActSpisForm, ActSpisItemFormSet
from .models import ActSpis
from products.models import Product
from employees.models import Employee


class ProductUnitsMixin:
	@staticmethod
	def get_product_units():
		return {
			str(item['id']): item['unit__name'] or ''
			for item in Product.objects.select_related('unit').values('id', 'unit__name')
		}

	@staticmethod
	def get_employee_positions():
		return {
			str(item['id']): item['position__name'] or ''
			for item in Employee.objects.select_related('position').values('id', 'position__name')
		}

	def inject_product_units(self, context):
		units_map = self.get_product_units()
		context['product_units_json'] = json.dumps(units_map, ensure_ascii=False)
		return context

	def inject_employee_positions(self, context):
		positions_map = self.get_employee_positions()
		context['employee_positions_json'] = json.dumps(positions_map, ensure_ascii=False)
		return context


class ActSpisListView(ListView):
	model = ActSpis
	template_name = 'act_spis/list.html'
	context_object_name = 'acts'

	def get_queryset(self):
		return (
			ActSpis.objects.select_related('customer', 'chairperson__position')
			.annotate(
				total_amount=Coalesce(
					Sum('items__total'),
					Value(Decimal('0.00'), output_field=DecimalField(max_digits=12, decimal_places=2)),
				)
			)
			.order_by('-date', '-id')
		)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['page_title'] = 'Акты списания материальных ценностей'
		return context


class ActSpisCreateView(ProductUnitsMixin, SuccessMessageMixin, CreateView):
	model = ActSpis
	template_name = 'act_spis/create.html'
	form_class = ActSpisForm
	success_url = reverse_lazy('act_spis:list')
	success_message = 'Акт списания материальных ценностей успешно создан.'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = ActSpisItemFormSet(self.request.POST)
		else:
			context['formset'] = ActSpisItemFormSet()
		context['page_title'] = 'Создание акта списания материальных ценностей'
		context = self.inject_product_units(context)
		context = self.inject_employee_positions(context)
		return context

	def form_valid(self, form):
		context = self.get_context_data()
		formset = context['formset']
		if formset.is_valid():
			self.object = form.save()
			formset.instance = self.object
			formset.save()
			return super().form_valid(form)
		return self.render_to_response(self.get_context_data(form=form))


class ActSpisUpdateView(ProductUnitsMixin, SuccessMessageMixin, UpdateView):
	model = ActSpis
	template_name = 'act_spis/edit.html'
	form_class = ActSpisForm
	success_url = reverse_lazy('act_spis:list')
	success_message = 'Акт списания материальных ценностей успешно обновлён.'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = ActSpisItemFormSet(self.request.POST, instance=self.object)
		else:
			context['formset'] = ActSpisItemFormSet(instance=self.object)
		context['page_title'] = 'Изменение Акта списания материальных ценностей'
		context = self.inject_product_units(context)
		context = self.inject_employee_positions(context)
		return context

	def form_valid(self, form):
		context = self.get_context_data()
		formset = context['formset']
		if formset.is_valid():
			self.object = form.save()
			formset.instance = self.object
			formset.save()
			return super().form_valid(form)
		return self.render_to_response(self.get_context_data(form=form))


class ActSpisDeleteView(DeleteView):
	model = ActSpis
	template_name = 'act_spis/delete.html'
	success_url = reverse_lazy('act_spis:list')

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.delete()
		messages.success(request, 'Акт списания материальных ценностей успешно удалён.')
		return HttpResponseRedirect(self.get_success_url())


class ActSpisDetailView(DetailView):
	model = ActSpis
	template_name = 'act_spis/view.html'
	context_object_name = 'act'

	def get_queryset(self):
		return (
			super()
			.get_queryset()
			.select_related('customer', 'chairperson__position')
			.prefetch_related('items__product__unit')
		)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['items'] = self.object.items.all()
		context['total_amount'] = self.object.items.aggregate(
			total=Coalesce(
				Sum('total'),
				Value(Decimal('0.00'), output_field=DecimalField(max_digits=12, decimal_places=2)),
			)
		)['total']
		context['page_title'] = f'Акт списания материальных ценностей № {self.object.id}'
		return context
