from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Organization

class OrganizationListView(ListView):
    model = Organization
    template_name = 'organizations/list.html'
    context_object_name = 'organizations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Организации'
        return context

class OrganizationCreateView(SuccessMessageMixin, CreateView):
    model = Organization
    template_name = 'organizations/create.html'
    fields = ['name', 'address', 'inn', 'kpp', 'account', 'chief', 'financial_chief']
    success_url = reverse_lazy('organizations:list')
    success_message = "Организация успешно создана."

class OrganizationUpdateView(SuccessMessageMixin, UpdateView):
    model = Organization
    template_name = 'organizations/edit.html'
    fields = ['name', 'address', 'inn', 'kpp', 'account', 'chief', 'financial_chief']
    success_url = reverse_lazy('organizations:list')
    success_message = "Организация успешно обновлена."

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'organizations/delete.html'
    success_url = reverse_lazy('organizations:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Организация успешно удалена.")
            return HttpResponseRedirect(self.get_success_url())
        except ProtectedError:
            messages.error(request, "Невозможно удалить организацию, так как она используется в других записях.")
            return HttpResponseRedirect(self.get_success_url())
