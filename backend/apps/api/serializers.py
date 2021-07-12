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
