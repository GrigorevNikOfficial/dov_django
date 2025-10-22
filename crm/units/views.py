from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Unit

class UnitListView(ListView):
    model = Unit
    template_name = 'units/list.html'
    context_object_name = 'units'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Единицы измерения'
        return context

class UnitCreateView(SuccessMessageMixin, CreateView):
    model = Unit
    template_name = 'units/create.html'
    fields = ['name']
    success_url = reverse_lazy('units:list')
    success_message = "Единица измерения успешно создана."

class UnitUpdateView(SuccessMessageMixin, UpdateView):
    model = Unit
    template_name = 'units/edit.html'
    fields = ['name']
    success_url = reverse_lazy('units:list')
    success_message = "Единица измерения успешно обновлена."

class UnitDeleteView(DeleteView):
    model = Unit
    template_name = 'units/delete.html'
    success_url = reverse_lazy('units:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Единица измерения успешно удалена.")
            return HttpResponseRedirect(self.get_success_url())
        except ProtectedError:
            messages.error(request, "Невозможно удалить единицу измерения, так как она используется в других записях.")
            return HttpResponseRedirect(self.get_success_url())
