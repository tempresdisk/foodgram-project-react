from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        model = CustomUser
        extra_kwargs = {
                'password': {'write_only': True}
        }
