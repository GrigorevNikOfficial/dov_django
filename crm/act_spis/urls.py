from django.urls import path

from .views import (
    ActSpisCreateView,
    ActSpisDeleteView,
    ActSpisDetailView,
    ActSpisListView,
    ActSpisUpdateView,
)

app_name = 'act_spis'

urlpatterns = [
    path('', ActSpisListView.as_view(), name='list'),
    path('create/', ActSpisCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', ActSpisUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ActSpisDeleteView.as_view(), name='delete'),
    path('view/<int:pk>/', ActSpisDetailView.as_view(), name='view'),
]
