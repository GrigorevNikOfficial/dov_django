from django.urls import path

from .views import (
    ServiceActCreateView,
    ServiceActDeleteView,
    ServiceActDetailView,
    ServiceActListView,
    ServiceActUpdateView,
)

app_name = 'service_acts'

urlpatterns = [
    path('', ServiceActListView.as_view(), name='list'),
    path('create/', ServiceActCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', ServiceActUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ServiceActDeleteView.as_view(), name='delete'),
    path('view/<int:pk>/', ServiceActDetailView.as_view(), name='view'),
]
