from django.db import models
from users.models import User
from django.core.exceptions import ValidationError 
class Product(models.Model):
    productName = models.CharField(max_length=255)
    cost = models.PositiveIntegerField()
    amountAvailable = models.PositiveIntegerField()
    seller = models.ForeignKey(User,on_delete=models.CASCADE,related_name='products')
    
    
    #This function make sure that the cost price is divisible by five
    def clean(self):
        if self.cost % 5 != 0:
            raise ValidationError({
                'The cost price must be divisible by five'
            })
   
