from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class PaymentOrder(models.Model):
    number = models.CharField("Номер", max_length=20)
    date = models.DateField("Дата")
    payment_kind = models.CharField("Вид платежа", max_length=20, blank=True)

    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.PROTECT,
        verbose_name="Плательщик",
        related_name='payment_orders',
    )
    payer_account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.PROTECT,
        verbose_name="Счёт плательщика",
        related_name='payment_orders_as_payer',
        null=True,
        blank=True,
    )
    payer_inn = models.CharField("ИНН плательщика", max_length=12, blank=True)
    payer_kpp = models.CharField("КПП плательщика", max_length=9, blank=True)

    recipient = models.ForeignKey(
        'customers.Customer',
        on_delete=models.PROTECT,
        verbose_name="Получатель",
        related_name='payment_orders',
    )
    recipient_account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.PROTECT,
        verbose_name="Счёт получателя",
        related_name='payment_orders_as_recipient',
        null=True,
        blank=True,
    )
    recipient_inn = models.CharField("ИНН получателя", max_length=12, blank=True)
    recipient_kpp = models.CharField("КПП получателя", max_length=9, blank=True)

    amount = models.DecimalField(
        "Сумма",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    amount_text = models.CharField("Сумма прописью", max_length=255, blank=True)

    payment_purpose = models.TextField("Назначение платежа")
    kbk = models.CharField("КБК", max_length=50, blank=True)
    oktmo = models.CharField("ОКТМО", max_length=50, blank=True)

    payment_operation_type = models.CharField("Вид оп.", max_length=4, blank=True, default='01')
    payment_due_date = models.CharField("Срок плат.", max_length=20, blank=True)
    payment_assignment_code = models.CharField("Наз. пл.", max_length=20, blank=True)
    payment_priority = models.CharField("Очеред. плат.", max_length=5, blank=True, default='5')
    payment_code = models.CharField("Код", max_length=5, blank=True, default='0')
    reserve_field = models.CharField("Рез. поле", max_length=20, blank=True)

    payment_basis = models.CharField("Основание платежа", max_length=50, blank=True)
    tax_period = models.CharField("Налоговый период", max_length=50, blank=True)
    doc_number = models.CharField("Номер документа", max_length=50, blank=True)
    doc_date = models.DateField("Дата документа", null=True, blank=True)

    def __str__(self):
        date_value = self.date.strftime('%d.%m.%Y') if self.date else ''
        return f"Платёжное поручение № {self.number} от {date_value}"

    def _default_amount_text(self) -> str:
        if self.amount is None:
            return ''
        quantized = self.amount.quantize(Decimal('0.01'))
        rubles = int(quantized)
        kopeks = int((quantized - Decimal(rubles)) * 100)
        formatted_rubles = f"{rubles:,}".replace(',', ' ')
        return f"{formatted_rubles} рублей {kopeks:02d} копеек"

    def save(self, *args, **kwargs):
        if self.organization:
            # Always sync payer account/INN/KPP from organization directory
            self.payer_account = getattr(self.organization, 'account', None)
            if not self.payer_inn:
                self.payer_inn = getattr(self.organization, 'inn', '') or ''
            if not self.payer_kpp:
                self.payer_kpp = getattr(self.organization, 'kpp', '') or ''

        if self.recipient:
            # Always sync recipient account/INN/KPP from customer directory
            self.recipient_account = getattr(self.recipient, 'account', None)
            if not self.recipient_inn:
                self.recipient_inn = getattr(self.recipient, 'inn', '') or ''
            if not self.recipient_kpp:
                self.recipient_kpp = getattr(self.recipient, 'kpp', '') or ''

        if self.amount and not self.amount_text:
            self.amount_text = self._default_amount_text()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Платёжное поручение"
        verbose_name_plural = "Платёжные поручения"
        ordering = ['-date', '-id']
