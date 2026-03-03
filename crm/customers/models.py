from django.db import models

class Customer(models.Model):
    name = models.CharField("Название", max_length=255)
    inn = models.CharField("ИНН", max_length=12, blank=True)
    kpp = models.CharField("КПП", max_length=9, blank=True)
    account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.PROTECT,
        verbose_name="Счёт",
        related_name='customers',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"
        ordering = ['name']
