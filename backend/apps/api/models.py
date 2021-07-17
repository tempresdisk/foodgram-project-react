from os import name
from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .fields import fields

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        unique=True,
        max_length=24
    )
    color = fields.ColorField(
        verbose_name=_('Цвет'),
        unique=True
    )
    slug = models.SlugField(
        verbose_name=_('Слаг'),
        unique=True
    )

    class Meta:
        app_label = 'api'
        verbose_name = _('Тэг')
        verbose_name_plural = _('Тэги')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        blank=False,
        max_length=50
    )
    measurement_unit = models.CharField(
        verbose_name=_('Единица измерения'),
        max_length=10,
        blank=False
    )

    class Meta:
        app_label = 'api'
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='subscribed_on')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='subscriber')

    class Meta:
        app_label = 'api'
        verbose_name = _('Подписка')
        verbose_name_plural = _('Подписки')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='subscribe'
            )
        ]
    
    def __str__(self):
        return (f'Подписка {self.user.username} на {self.author.username}')


class Recipe(models.Model):
    author = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='recipe')
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=30,
        blank=False
    )
    image = models.ImageField(
        verbose_name=_('Изображение'),
        upload_to='recipes/',
        blank=False,
    )
    text = models.TextField(
        verbose_name=_('Описание'),
        blank=False
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        blank=False,
        related_name='recipe',
        verbose_name=_('Ингредиенты')
    )
    tags = models.ManyToManyField(
        to=Tag,
        blank=False,
        related_name='recipe',
        verbose_name=_('Тэги')
    )
    cooking_time = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(1, message='минимальное время готовки 1 минута')
        ],
        blank=False,
        verbose_name=_('Время приготовления в минутах')
    )

    class Meta:
        app_label = 'api'
        verbose_name = _('Рецепт')
        verbose_name_plural = _('Рецепты')
    
    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amount'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount'
    )
    amount = models.PositiveIntegerField(
        validators=[validators.MinValueValidator(1)]
    )

    class Meta:
        app_label = 'api'
        verbose_name = _('Ингредиент-рецепт')
        verbose_name_plural = _('Ингредиент-рецепт')
    
    def __str__(self):
        return f'Количество {self.ingredient} в рецепте {self.recipe}'
