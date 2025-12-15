from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'role', 'deposit')
        read_only_fields = ('id', 'role', 'deposit')


    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.role != 'buyer':
            data.pop('deposit', None)

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user
