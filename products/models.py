from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError 
class Product(models.Model):
    productName = models.CharField(max_length=255)
    cost = models.PositiveIntegerField()
    amountAvailable = models.PositiveIntegerField()
    seller = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='products')

    def clean(self):
        if self.cost % 5 != 0:
            raise ValidationError({
                'The cost price must be divisible by five'
            })
   
