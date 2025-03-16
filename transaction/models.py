from django.db import models

# Create your models here.
class Transaction(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tig_id = models.IntegerField(default='-1')
    quantity = models.IntegerField(default='0')
    price = models.FloatField(default='0')

    class Meta:
        ordering = ('created',)