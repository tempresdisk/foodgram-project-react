from rest_framework import serializers

from . import models


class TagSerializer(serializers.ModelSerializer):

    class Meta():
        model = models.Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta():
        model = models.Ingredient
        fields = '__all__'
