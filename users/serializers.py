from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'role', 'deposit')
        read_only_fields = ('id', 'deposit')

    #make deposit hidden from the seller user
    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.role != 'buyer':
            data.pop('deposit', None)

        return data
    #validate the role to make sure it won't updated after created the user 
    def validate_role(self, value):
        if self.instance is not None:
            raise serializers.ValidationError("Role cannot be updated")
        return value
    
    

