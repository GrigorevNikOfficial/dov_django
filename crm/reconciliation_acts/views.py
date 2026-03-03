from decimal import Decimal

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ReconciliationActForm, ReconciliationActLineFormSet
from .models import ReconciliationAct


class ReconciliationActListView(ListView):
    model = ReconciliationAct
    template_name = 'reconciliation_acts/list.html'
    context_object_name = 'acts'

    def get_queryset(self):
        return (
            ReconciliationAct.objects
            .select_related('organization', 'customer')
            .prefetch_related('lines')
            .order_by('-date', '-id')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Акты сверки взаиморасчётов'
        return context


class ReconciliationActCreateView(SuccessMessageMixin, CreateView):
    model = ReconciliationAct
    form_class = ReconciliationActForm
    template_name = 'reconciliation_acts/create.html'
    success_url = reverse_lazy('reconciliation_acts:list')
    success_message = 'Акт сверки успешно создан.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ReconciliationActLineFormSet(self.request.POST)
        else:
            context['formset'] = ReconciliationActLineFormSet()
        context['page_title'] = 'Создание акта сверки'
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


class ReconciliationActUpdateView(SuccessMessageMixin, UpdateView):
    model = ReconciliationAct
    form_class = ReconciliationActForm
    template_name = 'reconciliation_acts/edit.html'
    success_url = reverse_lazy('reconciliation_acts:list')
    success_message = 'Акт сверки успешно обновлён.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ReconciliationActLineFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = ReconciliationActLineFormSet(instance=self.object)
        context['page_title'] = f'Редактирование акта сверки № {self.object.number}'
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


class ReconciliationActDeleteView(DeleteView):
    model = ReconciliationAct
    template_name = 'reconciliation_acts/delete.html'
    success_url = reverse_lazy('reconciliation_acts:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, 'Акт сверки удалён.')
        return HttpResponseRedirect(self.get_success_url())


class ReconciliationActDetailView(DetailView):
    model = ReconciliationAct
    template_name = 'reconciliation_acts/view.html'
    context_object_name = 'act'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lines = self.object.lines.all()
        total_debit = self.object.total_debit()
        total_credit = self.object.total_credit()
        total_customer_debit = self.object.total_customer_debit()
        total_customer_credit = self.object.total_customer_credit()
        org_open_debit = self.object.opening_balance or Decimal('0.00')
        org_open_credit = self.object.closing_balance or Decimal('0.00')
        cust_open_debit = self.object.opening_balance_customer or Decimal('0.00')
        cust_open_credit = self.object.closing_balance_customer or Decimal('0.00')

        org_net = (org_open_debit + total_debit) - (org_open_credit + total_credit)
        cust_net = (cust_open_debit + total_customer_debit) - (cust_open_credit + total_customer_credit)

        org_closing_debit = org_net if org_net > 0 else Decimal('0.00')
        org_closing_credit = abs(org_net) if org_net < 0 else Decimal('0.00')
        customer_closing_debit = cust_net if cust_net > 0 else Decimal('0.00')
        customer_closing_credit = abs(cust_net) if cust_net < 0 else Decimal('0.00')

        org_balance_line = "По данным {org}, на {date} задолженность на {status}.".format(
            org=self.object.organization.name,
            date=self.object.date.strftime('%d.%m.%Y'),
            status=(
                f"пользу {self.object.organization.name} — {org_closing_debit:.2f} рублей"
                if org_net > 0
                else f"пользу {self.object.customer.name} — {org_closing_credit:.2f} рублей"
                if org_net < 0
                else "отсутствует"
            ),
        )

        customer_balance_line = "По данным {cust}, на {date} задолженность на {status}.".format(
            cust=self.object.customer.name,
            date=self.object.date.strftime('%d.%m.%Y'),
            status=(
                f"пользу {self.object.customer.name} — {customer_closing_debit:.2f} рублей"
                if cust_net > 0
                else f"пользу {self.object.organization.name} — {customer_closing_credit:.2f} рублей"
                if cust_net < 0
                else "отсутствует"
            ),
        )
        context.update({
            'lines': lines,
            'total_debit': total_debit,
            'total_credit': total_credit,
            'total_customer_debit': total_customer_debit,
            'total_customer_credit': total_customer_credit,
            'org_closing': org_net,
            'customer_closing': cust_net,
            'org_closing_debit': org_closing_debit,
            'org_closing_credit': org_closing_credit,
            'customer_closing_debit': customer_closing_debit,
            'customer_closing_credit': customer_closing_credit,
            'closing_abs': abs(org_net),
            'customer_closing_abs': abs(cust_net),
            'org_closing_display': f"{org_closing_debit or org_closing_credit:.2f}",
            'customer_closing_display': f"{customer_closing_debit or customer_closing_credit:.2f}",
            'org_balance_line': org_balance_line,
            'customer_balance_line': customer_balance_line,
            'page_title': f'Акт сверки № {self.object.number}',
        })
        return context
