from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('seller',) #to make sure that the selller can not updated
        
        
    #ovride the function to make the id hidden for the buyers
    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.user.role == 'buyer':
            data.pop('id', None)

        return data

