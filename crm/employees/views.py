from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Employee

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employees/list.html'
    context_object_name = 'employees'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Сотрудники'
        return context

class EmployeeCreateView(SuccessMessageMixin, CreateView):
    model = Employee
    template_name = 'employees/create.html'
    fields = ['last_name', 
              'first_name', 
              'middle_name', 
              'position', 
              'passport_series', 
              'passport_number', 
              'passport_issued_by', 
              'passport_issue_date']
    success_url = reverse_lazy('employees:list')
    success_message = "Сотрудник успешно создан."

class EmployeeUpdateView(SuccessMessageMixin, UpdateView):
    model = Employee
    template_name = 'employees/edit.html'
    fields = ['last_name', 
              'first_name',
              'middle_name', 
              'position', 
              'passport_series', 
              'passport_number', 
              'passport_issued_by', 
              'passport_issue_date']
    success_url = reverse_lazy('employees:list')
    success_message = "Сотрудник успешно обновлён."

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'employees/delete.html'
    success_url = reverse_lazy('employees:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Сотрудник успешно удалён.")
            return HttpResponseRedirect(self.get_success_url())
        except ProtectedError:
            messages.error(request, "Невозможно удалить сотрудника, так как он используется в других записях.")
            return HttpResponseRedirect(self.get_success_url())
