from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Position

class PositionListView(ListView):
    model = Position
    template_name = 'positions/list.html'
    context_object_name = 'positions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Должности'
        return context

class PositionCreateView(SuccessMessageMixin, CreateView):
    model = Position
    template_name = 'positions/create.html'
    fields = ['name']
    success_url = reverse_lazy('positions:list')
    success_message = "Должность успешно создана."

class PositionUpdateView(SuccessMessageMixin, UpdateView):
    model = Position
    template_name = 'positions/edit.html'
    fields = ['name']
    success_url = reverse_lazy('positions:list')
    success_message = "Должность успешно обновлена."

class PositionDeleteView(DeleteView):
    model = Position
    template_name = 'positions/delete.html'
    success_url = reverse_lazy('positions:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Должность успешно удалена.")
            return HttpResponseRedirect(self.get_success_url())
        except ProtectedError:
            messages.error(request, "Невозможно удалить должность, так как она используется в других записях.")
            return HttpResponseRedirect(self.get_success_url())
