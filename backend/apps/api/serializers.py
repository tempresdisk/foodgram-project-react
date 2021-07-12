from re import U
from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models
from ..users.serializers import UserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta():
        model = models.Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta():
        model = models.Ingredient
        fields = ('id', 'name', 'measurement_unit')


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta():
        model = models.Subscription
        fields = ('user',)

'''
class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all()
    )
    username = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    first_name = serializers.SlugRelatedField(
        slug_field='first_name',
        queryset=User.objects.all()
    )
    last_name = serializers.SlugRelatedField(
        slug_field='last_name',
        queryset=User.objects.all()
    )

    class Meta():
        model = models.Subscription
        fields = ('username', 'email', 'first_name', 'last_name')
        read_only_fields = ('username', 'email', 'first_name', 'last_name')
'''
