from django.db import models
from django.core.validators import MinValueValidator

class Proxy(models.Model):
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.PROTECT,
        verbose_name="Организация",
        related_name="proxies",
    )
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.PROTECT,
        verbose_name="Сотрудник",
        related_name="proxies",
    )
    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.PROTECT,
        verbose_name="Контрагент",
        related_name="proxies",
    )
    date_of_issue = models.DateField("Дата выдачи")
    is_valid_until = models.DateField("Действителен до")


    def __str__(self):
        return f"Доверенность № {self.id}"

    class Meta:
        verbose_name = "Доверенность"
        verbose_name_plural = "Доверенности"
        ordering = ['-date_of_issue']

class ProxyItem(models.Model):
    proxy = models.ForeignKey(
        'proxies.Proxy',
        on_delete=models.CASCADE,
        verbose_name="Доверенность",
        related_name="items",
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        verbose_name="Товар",
    )
    amount = models.PositiveIntegerField("Количество", validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = "Элемент доверенности"
        verbose_name_plural = "Элементы доверенности"
        ordering = ['id']
