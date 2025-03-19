from datetime import datetime

from django.db import models


# Create your models here.
class Transaction(models.Model):
    TYPE_CHOICES = [
        ('ajout', 'ajout'),
        ('retraitVente', 'retrait par vente'),
        ('retraitInvendus', 'retrait par invendus'),
    ]

    created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(default=datetime.now)
    tig_id = models.IntegerField(default='-1')
    category = models.IntegerField(default='-1')
    quantity = models.IntegerField(default='0')
    price = models.FloatField(default='0')
    onSale = models.BooleanField(default=False)
    type = models.CharField(
        max_length=15,
        choices=TYPE_CHOICES,
        default='ajout'
    )

    def get_revenue(self):
        """Retourne le chiffre d'affaires de la transaction uniquement si c'est une vente"""
        print('ICIlol: ',self.type)
        return self.price if self.type == 'retraitVente' else 0

    class Meta:
        ordering = ('created',)
