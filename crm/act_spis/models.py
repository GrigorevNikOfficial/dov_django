from decimal import Decimal, ROUND_HALF_UP

from django.core.validators import MinValueValidator
from django.db import models


class ActSpis(models.Model):
	date = models.DateField("Дата")
	customer = models.ForeignKey(
		'customers.Customer',
		on_delete=models.PROTECT,
		verbose_name="Контрагент",
		related_name='write_off_acts',
	)
	contract = models.CharField("Договор", max_length=255, blank=True)
	warehouse = models.CharField("Склад", max_length=255)
	# chairperson is a FK to Employee; we store the chairperson (employee) and snapshot the
	# employee's position for display. Previously this was called 'responsible_employee'.
	chairperson = models.ForeignKey(
		'employees.Employee',
		on_delete=models.PROTECT,
		verbose_name="Председатель комиссии",
		related_name='write_off_acts',
		blank=True,
		null=True,
	)

	class Meta:
		verbose_name = "Акт списания материальных ценностей"
		verbose_name_plural = "Акты списания материальных ценностей"
		ordering = ['-date', '-id']

	def __str__(self):
		return f"Акт списания материальных ценностей № {self.id}"


class ActSpisItem(models.Model):
	act = models.ForeignKey(
		'act_spis.ActSpis',
		on_delete=models.CASCADE,
		verbose_name="Акт списания материальных ценностей",
		related_name='items',
	)
	product = models.ForeignKey(
		'products.Product',
		on_delete=models.PROTECT,
		verbose_name="Товар",
	)
	quantity = models.DecimalField(
		"Количество",
		max_digits=10,
		decimal_places=2,
		validators=[MinValueValidator(Decimal('0.01'))],
	)
	price = models.DecimalField(
		"Цена",
		max_digits=12,
		decimal_places=2,
		validators=[MinValueValidator(Decimal('0.00'))],
	)
	total = models.DecimalField(
		"Сумма",
		max_digits=12,
		decimal_places=2,
		editable=False,
		default=Decimal('0.00'),
	)
	unit_name = models.CharField("Единица измерения", max_length=50, blank=True)

	class Meta:
		verbose_name = "Позиция акта списания материальных ценностей"
		verbose_name_plural = "Позиции акта списания материальных ценностей"
		ordering = ['id']

	def __str__(self):
		return f"{self.product} ({self.quantity} × {self.price})"

	def save(self, *args, **kwargs):
		if self.product_id:
			unit_value = getattr(self.product.unit, 'name', '')
			self.unit_name = unit_value
		if self.quantity is not None and self.price is not None:
			self.total = (self.quantity * self.price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
		else:
			self.total = Decimal('0.00')
		super().save(*args, **kwargs)
