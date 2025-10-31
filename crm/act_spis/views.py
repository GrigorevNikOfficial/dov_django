from decimal import Decimal

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import DecimalField, Sum, Value
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ActSpisForm, ActSpisItemFormSet
from .models import ActSpis


class ActSpisListView(ListView):
	model = ActSpis
	template_name = 'act_spis/list.html'
	context_object_name = 'acts'

	def get_queryset(self):
		return (
			ActSpis.objects.select_related('customer')
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
		context['page_title'] = 'Акты списания'
		return context


class ActSpisCreateView(SuccessMessageMixin, CreateView):
	model = ActSpis
	template_name = 'act_spis/create.html'
	form_class = ActSpisForm
	success_url = reverse_lazy('act_spis:list')
	success_message = 'Акт списания успешно создан.'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = ActSpisItemFormSet(self.request.POST)
		else:
			context['formset'] = ActSpisItemFormSet()
		context['page_title'] = 'Создание акта списания'
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


class ActSpisUpdateView(SuccessMessageMixin, UpdateView):
	model = ActSpis
	template_name = 'act_spis/edit.html'
	form_class = ActSpisForm
	success_url = reverse_lazy('act_spis:list')
	success_message = 'Акт списания успешно обновлён.'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.POST:
			context['formset'] = ActSpisItemFormSet(self.request.POST, instance=self.object)
		else:
			context['formset'] = ActSpisItemFormSet(instance=self.object)
		context['page_title'] = 'Редактирование акта списания'
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
		messages.success(request, 'Акт списания успешно удалён.')
		return HttpResponseRedirect(self.get_success_url())


class ActSpisDetailView(DetailView):
	model = ActSpis
	template_name = 'act_spis/view.html'
	context_object_name = 'act'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['items'] = self.object.items.select_related('product__unit')
		context['total_amount'] = self.object.items.aggregate(
			total=Coalesce(
				Sum('total'),
				Value(Decimal('0.00'), output_field=DecimalField(max_digits=12, decimal_places=2)),
			)
		)['total']
		context['page_title'] = f'Акт списания № {self.object.id}'
		return context
