from django.apps import AppConfig


class PaymentOrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment_orders'
    verbose_name = 'Платёжные поручения'
