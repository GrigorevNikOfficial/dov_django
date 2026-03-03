from django.urls import path

from .views import (
    ReconciliationActCreateView,
    ReconciliationActDeleteView,
    ReconciliationActDetailView,
    ReconciliationActListView,
    ReconciliationActUpdateView,
)

app_name = 'reconciliation_acts'

urlpatterns = [
    path('', ReconciliationActListView.as_view(), name='list'),
    path('create/', ReconciliationActCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', ReconciliationActUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ReconciliationActDeleteView.as_view(), name='delete'),
    path('view/<int:pk>/', ReconciliationActDetailView.as_view(), name='view'),
]
