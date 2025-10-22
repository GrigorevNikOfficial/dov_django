from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Proxy, ProxyItem
from .forms import ProxyForm, ProxyItemFormSet

class ProxyListView(ListView):
    model = Proxy
    template_name = 'proxies/list.html'
    context_object_name = 'proxies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Доверенности'
        return context
    
    def get_queryset(self):
        return Proxy.objects.select_related('organization', 'employee', 'customer').order_by('-date_of_issue')

class ProxyCreateView(SuccessMessageMixin, CreateView):
    model = Proxy
    template_name = 'proxies/create.html'
    form_class = ProxyForm
    success_url = reverse_lazy('proxies:list')
    success_message = "Доверенность успешно создана."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ProxyItemFormSet(self.request.POST)
        else:
            context['formset'] = ProxyItemFormSet()
        context['page_title'] = 'Создание доверенности'
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ProxyUpdateView(SuccessMessageMixin, UpdateView):
    model = Proxy
    template_name = 'proxies/edit.html'
    form_class = ProxyForm
    success_url = reverse_lazy('proxies:list')
    success_message = "Доверенность успешно обновлена."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ProxyItemFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = ProxyItemFormSet(instance=self.object)
        context['page_title'] = 'Редактирование доверенности'
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ProxyDeleteView(DeleteView):
    model = Proxy
    template_name = 'proxies/delete.html'
    success_url = reverse_lazy('proxies:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, "Доверенность успешно удалена.")
            return HttpResponseRedirect(self.get_success_url())
        except ProtectedError:
            messages.error(request, "Невозможно удалить доверенность, так как она используется в других записях.")
            return HttpResponseRedirect(self.get_success_url())

class ProxyDetailView(DetailView):
    model = Proxy
    template_name = 'proxies/view.html'
    context_object_name = 'proxy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.select_related('product__unit')
        context['page_title'] = f'Доверенность № {self.object.id}'
        return context
