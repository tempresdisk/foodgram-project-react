from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_subscribed', 'password')
        model = CustomUser
        extra_kwargs = {
                'password': {'write_only': True}
        }

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.subscriber.filter(user=user).exists()
