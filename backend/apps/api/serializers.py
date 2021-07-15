from re import U
from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta():
        model = models.Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta():
        model = models.Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta():
        model = models.Recipe
        fields = '__all__'
