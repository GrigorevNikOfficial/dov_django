from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum


class ReconciliationAct(models.Model):
    number = models.CharField("Номер", max_length=50)
    date = models.DateField("Дата")
    period_from = models.DateField("Период с")
    period_to = models.DateField("Период по")

    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.PROTECT,
        verbose_name="Организация",
        related_name='reconciliation_acts',
    )
    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.PROTECT,
        verbose_name="Контрагент",
        related_name='reconciliation_acts',
    )

    opening_balance = models.DecimalField(
        "Входящее сальдо",
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    closing_balance = models.DecimalField(
        "Исходящее сальдо",
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    opening_balance_customer = models.DecimalField(
        "Входящее сальдо (контрагент)",
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    closing_balance_customer = models.DecimalField(
        "Исходящее сальдо (контрагент)",
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00'),
    )
    note = models.TextField("Примечание", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        date_value = self.date.strftime('%d.%m.%Y') if self.date else ''
        return f"Акт сверки № {self.number} от {date_value}"

    def total_debit(self) -> Decimal:
        return self.lines.aggregate(total=Sum('debit'))['total'] or Decimal('0.00')

    def total_credit(self) -> Decimal:
        return self.lines.aggregate(total=Sum('credit'))['total'] or Decimal('0.00')

    def total_customer_debit(self) -> Decimal:
        return self.lines.aggregate(total=Sum('customer_debit'))['total'] or Decimal('0.00')

    def total_customer_credit(self) -> Decimal:
        return self.lines.aggregate(total=Sum('customer_credit'))['total'] or Decimal('0.00')

    def recalculate_closing_balance(self) -> None:
        opening = self.opening_balance or Decimal('0.00')
        debit_total = self.total_debit()
        credit_total = self.total_credit()
        self.closing_balance = opening + debit_total - credit_total
        self.save(update_fields=['closing_balance'])

    class Meta:
        verbose_name = "Акт сверки"
        verbose_name_plural = "Акты сверки взаиморасчётов"
        ordering = ['-date', '-id']


class ReconciliationActLine(models.Model):
    act = models.ForeignKey(
        ReconciliationAct,
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name="Акт",
    )
    order = models.PositiveIntegerField("Порядок", default=0)
    date = models.DateField("Дата", null=True, blank=True)
    document = models.CharField("Документ", max_length=255, blank=True)
    debit = models.DecimalField(
        "Дебет организации",
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    credit = models.DecimalField(
        "Кредит организации",
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    customer_debit = models.DecimalField(
        "Дебет контрагента",
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    customer_credit = models.DecimalField(
        "Кредит контрагента",
        max_digits=14,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    comment = models.CharField("Комментарий", max_length=255, blank=True)

    class Meta:
        verbose_name = "Строка акта сверки"
        verbose_name_plural = "Строки акта сверки"
        ordering = ['order', 'date', 'id']

    def __str__(self):
        return self.document or f"Строка {self.pk}"
