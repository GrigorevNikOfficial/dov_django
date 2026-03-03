from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PaymentOrderForm
from .models import PaymentOrder


class PaymentOrderListView(ListView):
    model = PaymentOrder
    template_name = 'payment_orders/list.html'
    context_object_name = 'payment_orders'

    def get_queryset(self):
        return (
            PaymentOrder.objects
            .select_related('organization', 'recipient', 'payer_account', 'recipient_account')
            .order_by('-date', '-id')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Платёжные поручения'
        return context


class PaymentOrderCreateView(SuccessMessageMixin, CreateView):
    model = PaymentOrder
    form_class = PaymentOrderForm
    template_name = 'payment_orders/create.html'
    success_url = reverse_lazy('payment_orders:list')
    success_message = 'Платёжное поручение успешно создано.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Создание платёжного поручения'
        return context


class PaymentOrderUpdateView(SuccessMessageMixin, UpdateView):
    model = PaymentOrder
    form_class = PaymentOrderForm
    template_name = 'payment_orders/edit.html'
    success_url = reverse_lazy('payment_orders:list')
    success_message = 'Платёжное поручение успешно обновлено.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Редактирование платёжного поручения № {self.object.number}'
        return context


class PaymentOrderDeleteView(DeleteView):
    model = PaymentOrder
    template_name = 'payment_orders/delete.html'
    success_url = reverse_lazy('payment_orders:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, 'Платёжное поручение успешно удалено.')
            return HttpResponseRedirect(self.get_success_url())
        except ProtectedError:
            messages.error(request, 'Невозможно удалить платёжное поручение, так как оно используется в других записях.')
            return HttpResponseRedirect(self.get_success_url())


class PaymentOrderDetailView(DetailView):
    model = PaymentOrder
    template_name = 'payment_orders/view.html'
    context_object_name = 'payment_order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Платёжное поручение № {self.object.number}'
        return context
