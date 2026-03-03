from django.db import models

class Account(models.Model):
    account = models.CharField("Номер счёта", max_length=100)
    bank_name = models.CharField("Банк", max_length=200)
    bank_identification_number = models.CharField("БИК", max_length=50)
    correspondent_account = models.CharField("Корреспондентский счёт", max_length=100, blank=True)

    def __str__(self):
        return f"{self.account} - {self.bank_name}".strip()
    
    class Meta:
        verbose_name = "Банковский счёт"
        verbose_name_plural = "Банковские счета"
        ordering = ['bank_name']
