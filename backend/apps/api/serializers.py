import base64
import six
import uuid
import imghdr
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.files.base import ContentFile

from . import models
from ..users.serializers import UserSerializer

User = get_user_model()


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')
            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)
        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension


class TagSerializer(serializers.ModelSerializer):

    class Meta():
        model = models.Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientReadSerializer(serializers.ModelSerializer):

    class Meta():
        model = models.Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class IngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta():
        model = models.Ingredient
        fields = ('id', 'amount')
    
    def validate_amount(self, value):
        """
        Check that the value is >= 0
        """
        if value < 0:
            raise serializers.ValidationError('amount must be positive.')
        return value


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')  # noqa E501

    class Meta():
        model = models.RecipeIngredient
        fields = ('id', 'name', 'amount', 'measurement_unit')
        read_only_fields = ('amount',)


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientReadSerializer(source='amount', many=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta():
        model = models.Recipe
        fields = ('id', 'author', 'name', 'text', 'image',
                  'ingredients', 'tags', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.is_favorited.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return obj.is_in_shopping_cart.filter(user=user).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = IngredientWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=models.Tag.objects.all(), many=True
    )

    class Meta():
        model = models.Recipe
        fields = ('id', 'author', 'name', 'text', 'image',
                  'ingredients', 'tags', 'cooking_time')
        extra_kwargs = {
            'ingredients': {
                'error_messages': {
                    'amount': ('Минимальное количество должно быть не менее 0'),
                }
            }
        }

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = models.Recipe.objects.create(**validated_data)

        for ingredient in ingredients_data:
            amount = ingredient['amount']
            id = ingredient['id']
            models.RecipeIngredient.objects.create(
                ingredient=models.Ingredient.objects.get(id=id),
                recipe=recipe, amount=amount
            )
        for tag in tags_data:
            recipe.tags.add(tag)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.image = validated_data.get('image')
        instance.cooking_time = validated_data.get('cooking_time')

        models.RecipeIngredient.objects.filter(recipe=instance).delete()

        for ingredient in ingredients_data:
            amount = ingredient['amount']
            id = ingredient['id']
            models.RecipeIngredient.objects.create(
                ingredient=models.Ingredient.objects.get(id=id),
                recipe=instance, amount=amount
            )
        for tag in tags_data:
            instance.tags.add(tag)

        instance.save()
        return instance

    def to_representation(self, instance):
        data = RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data
        return data


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta():
        model = models.Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
