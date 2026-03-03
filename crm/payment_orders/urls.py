from django.urls import path

from .views import (
    PaymentOrderCreateView,
    PaymentOrderDeleteView,
    PaymentOrderDetailView,
    PaymentOrderListView,
    PaymentOrderUpdateView,
)

app_name = 'payment_orders'

urlpatterns = [
    path('', PaymentOrderListView.as_view(), name='list'),
    path('create/', PaymentOrderCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', PaymentOrderUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', PaymentOrderDeleteView.as_view(), name='delete'),
    path('view/<int:pk>/', PaymentOrderDetailView.as_view(), name='view'),
]
