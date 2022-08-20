from unicodedata import category
from django.db import models


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    local_currency = models.CharField(max_length=10)
    notes = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    description = models.CharField(max_length=300)