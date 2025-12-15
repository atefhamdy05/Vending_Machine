from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    BUYER = 'buyer'
    SELLER = 'seller'

    ROLE_CHOICES = [
        (BUYER, 'Buyer'),
        (SELLER, 'Seller'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    deposit = models.PositiveIntegerField(default=0)
