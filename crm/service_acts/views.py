from decimal import Decimal

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ServiceActForm, ServiceActLineFormSet
from .models import ServiceAct


class ServiceActListView(ListView):
    model = ServiceAct
    template_name = 'service_acts/list.html'
    context_object_name = 'acts'

    def get_queryset(self):
        return (
            ServiceAct.objects
            .select_related('executor', 'customer')
            .prefetch_related('lines')
            .order_by('-date', '-id')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Акты выполненных работ'
        return context


class ServiceActCreateView(SuccessMessageMixin, CreateView):
    model = ServiceAct
    form_class = ServiceActForm
    template_name = 'service_acts/create.html'
    success_url = reverse_lazy('service_acts:list')
    success_message = 'Акт успешно создан.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ServiceActLineFormSet(self.request.POST)
        else:
            context['formset'] = ServiceActLineFormSet()
        context['page_title'] = 'Создание акта выполненных работ'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if not formset.is_valid():
            return self.form_invalid(form)
        with transaction.atomic():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())


class ServiceActUpdateView(SuccessMessageMixin, UpdateView):
    model = ServiceAct
    form_class = ServiceActForm
    template_name = 'service_acts/edit.html'
    success_url = reverse_lazy('service_acts:list')
    success_message = 'Акт успешно обновлён.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ServiceActLineFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = ServiceActLineFormSet(instance=self.object)
        context['page_title'] = f'Редактирование акта выполненных работ № {self.object.number}'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if not formset.is_valid():
            return self.form_invalid(form)
        with transaction.atomic():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())


class ServiceActDeleteView(DeleteView):
    model = ServiceAct
    template_name = 'service_acts/delete.html'
    success_url = reverse_lazy('service_acts:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, 'Акт удалён.')
            return HttpResponseRedirect(self.get_success_url())
        except ProtectedError:
            messages.error(request, 'Невозможно удалить акт, так как он используется в других записях.')
            return HttpResponseRedirect(self.get_success_url())


class ServiceActDetailView(DetailView):
    model = ServiceAct
    template_name = 'service_acts/view.html'
    context_object_name = 'act'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        act = self.object
        lines = act.lines.all()
        context.update({
            'lines': lines,
            'total_without_vat': act.total_without_vat,
            'vat_amount': act.vat_amount,
            'total_with_vat': act.total_with_vat,
            'page_title': f'Акт выполненных работ № {act.number}',
        })
        return context
