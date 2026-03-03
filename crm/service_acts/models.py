from decimal import Decimal, ROUND_HALF_UP

from django.db import models


class ServiceAct(models.Model):
    number = models.CharField("Номер", max_length=50)
    date = models.DateField("Дата")
    executor = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.PROTECT,
        related_name='service_acts_as_executor',
        verbose_name="Исполнитель",
    )
    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.PROTECT,
        related_name='service_acts',
        verbose_name="Заказчик",
    )
    note = models.TextField("Примечание", blank=True)

    def __str__(self):
        date_value = self.date.strftime('%d.%m.%Y') if self.date else ''
        return f"Акт № {self.number} от {date_value}"

    def _quantize_money(self, value: Decimal) -> Decimal:
        return (value or Decimal('0.00')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def total_without_vat(self) -> Decimal:
        total = Decimal('0.00')
        for line in self.lines.all():
            total += line.amount_without_vat
        return self._quantize_money(total)

    @property
    def vat_amount(self) -> Decimal:
        total = Decimal('0.00')
        for line in self.lines.all():
            total += line.vat_amount
        return self._quantize_money(total)

    @property
    def total_with_vat(self) -> Decimal:
        return self._quantize_money(self.total_without_vat + self.vat_amount)

    class Meta:
        verbose_name = "Акт выполненных работ"
        verbose_name_plural = "Акты выполненных работ"
        ordering = ['-date', '-id']


class ServiceActLine(models.Model):
    act = models.ForeignKey(
        ServiceAct,
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name="Акт",
    )
    order = models.PositiveIntegerField("№", default=1)
    name = models.CharField("Наименование работы (услуги)", max_length=255)
    unit = models.CharField("Ед. изм.", max_length=32, blank=True, default='шт.')
    quantity = models.DecimalField("Количество", max_digits=10, decimal_places=3, default=Decimal('0.000'))
    price = models.DecimalField("Цена", max_digits=12, decimal_places=2, default=Decimal('0.00'))
    vat_rate = models.DecimalField("Ставка НДС, %", max_digits=5, decimal_places=2, default=Decimal('0.00'))

    def _quantize_money(self, value: Decimal) -> Decimal:
        return (value or Decimal('0.00')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def amount_without_vat(self) -> Decimal:
        if self.quantity is None or self.price is None:
            return Decimal('0.00')
        raw = self.quantity * self.price
        return self._quantize_money(raw)

    @property
    def vat_amount(self) -> Decimal:
        if not self.vat_rate:
            return Decimal('0.00')
        base = self.amount_without_vat
        return self._quantize_money(base * (self.vat_rate / Decimal('100')))

    @property
    def amount_with_vat(self) -> Decimal:
        return self._quantize_money(self.amount_without_vat + self.vat_amount)

    def __str__(self):
        return f"{self.order}. {self.name}"

    class Meta:
        verbose_name = "Строка акта"
        verbose_name_plural = "Строки акта"
        ordering = ['order', 'id']
