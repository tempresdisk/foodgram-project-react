from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from . import models
from .fields import fields


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'
    list_filter = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    formfield_overrides = {
        fields.ColorField: {'widget': forms.TextInput(attrs={'type': 'color',
                            'style': 'height: 100px; width: 100px;'})}
    }


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'image_tag')
    search_fields = ('user', 'author')
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('image_tag',)

    def image_tag(self, instance):
        return format_html(
            '<img src="{0}" style="max-width: 40%"/>',
            instance.image.url
        )

    image_tag.short_description = 'Предпросмотр изображения'
