from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Customer

class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/list.html'
    context_object_name = 'customers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Контрагенты'
        return context

class CustomerCreateView(SuccessMessageMixin, CreateView):
    model = Customer
    template_name = 'customers/create.html'
    fields = ['name', 'inn', 'kpp', 'account']
    success_url = reverse_lazy('customers:list')
    success_message = "Контрагент успешно создан."

class CustomerUpdateView(SuccessMessageMixin, UpdateView):
    model = Customer
    template_name = 'customers/edit.html'
    fields = ['name', 'inn', 'kpp', 'account']
    success_url = reverse_lazy('customers:list')
    success_message = "Контрагент успешно обновлён."

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customers/delete.html'
    success_url = reverse_lazy('customers:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Контрагент успешно удалён.")
            return HttpResponseRedirect(self.get_success_url())
        except ProtectedError:
            messages.error(request, "Невозможно удалить контрагента, так как он используется в других записях.")
            return HttpResponseRedirect(self.get_success_url())
