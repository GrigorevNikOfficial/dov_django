from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Account

class AccountListView(ListView):
    model = Account
    template_name = 'accounts/list.html'
    context_object_name = 'accounts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Банковские счета'
        return context

class AccountCreateView(SuccessMessageMixin, CreateView):
    model = Account
    template_name = 'accounts/create.html'
    fields = ['account', 'bank_name', 'bank_identification_number', 'correspondent_account']
    success_url = reverse_lazy('accounts:list')
    success_message = "Банковский счёт успешно создан."

class AccountUpdateView(SuccessMessageMixin, UpdateView):
    model = Account
    template_name = 'accounts/edit.html'
    fields = ['account', 'bank_name', 'bank_identification_number', 'correspondent_account']
    success_url = reverse_lazy('accounts:list')
    success_message = "Банковский счёт успешно обновлён."

class AccountDeleteView(DeleteView):
    model = Account
    template_name = 'accounts/delete.html'
    success_url = reverse_lazy('accounts:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Банковский счёт успешно удалён.")
            return HttpResponseRedirect(self.get_success_url())
        except ProtectedError:
            messages.error(request, "Невозможно удалить банковский счёт, так как он используется в других записях.")
            return HttpResponseRedirect(self.get_success_url())
