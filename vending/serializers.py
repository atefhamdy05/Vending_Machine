from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    seller = serializers.StringRelatedField()
    buyer = serializers.StringRelatedField()

    class Meta:
        model = Transaction
        fields = (
            'id',
            'product_name',
            'seller',
            'buyer',
            'amount',
            'total_spent',
            'created_at'
        )
