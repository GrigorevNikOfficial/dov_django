from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Товары'
        return context

class ProductCreateView(SuccessMessageMixin, CreateView):
    model = Product
    template_name = 'products/create.html'
    fields = ['name', 'price', 'unit']
    success_url = reverse_lazy('products:list')
    success_message = "Товар успешно создан."

class ProductUpdateView(SuccessMessageMixin, UpdateView):
    model = Product
    template_name = 'products/edit.html'
    fields = ['name', 'price', 'unit']
    success_url = reverse_lazy('products:list')
    success_message = "Товар успешно обновлён."

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/delete.html'
    success_url = reverse_lazy('products:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Товар успешно удалён.")
            return HttpResponseRedirect(self.get_success_url())
        except ProtectedError:
            messages.error(request, "Невозможно удалить товар, так как он используется в других записях.")
            return HttpResponseRedirect(self.get_success_url())
