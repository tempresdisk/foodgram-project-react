import pytest
from django.apps import apps as django_apps


@pytest.fixture
def vodka():
    Ingredient = django_apps.get_model('api.Ingredient', require_ready=True)
    Ingredient.objects.create(
        name='водка', measurement_unit='г'
    )
    vodka = Ingredient.objects.get(name='водка')
    return vodka


@pytest.fixture
def pickle():
    Ingredient = django_apps.get_model('api.Ingredient', require_ready=True)
    Ingredient.objects.create(
        name='огурец маринованный', measurement_unit='г'
    )
    pickle = Ingredient.objects.get(name='огурец маринованный')
    return pickle
