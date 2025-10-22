from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Department

class DepartmentListView(ListView):
    model = Department
    template_name = 'departments/list.html'
    context_object_name = 'departments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Отделы'
        return context

class DepartmentCreateView(SuccessMessageMixin, CreateView):
    model = Department
    template_name = 'departments/create.html'
    fields = ['name']
    success_url = reverse_lazy('departments:list')
    success_message = "Отдел успешно создан."

class DepartmentUpdateView(SuccessMessageMixin, UpdateView):
    model = Department
    template_name = 'departments/edit.html'
    fields = ['name']
    success_url = reverse_lazy('departments:list')
    success_message = "Отдел успешно обновлен."

class DepartmentDeleteView(DeleteView):
    model = Department
    template_name = 'departments/delete.html'
    success_url = reverse_lazy('departments:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Отдел успешно удалён.")
            return HttpResponseRedirect(self.get_success_url())
        except ProtectedError:
            messages.error(request, "Невозможно удалить отдел, так как он используется в других записях.")
            return HttpResponseRedirect(self.get_success_url())
