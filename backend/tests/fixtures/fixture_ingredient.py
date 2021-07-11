import pytest
from django.apps import apps as django_apps


@pytest.fixture
def ingredient():
    Ingredient = django_apps.get_model('api.Ingredient', require_ready=True)
    Ingredient.objects.create(
        name='ingredient_fixture', measurement_unit='g'
    )
    ingredient = Ingredient.objects.get(name='ingredient_fixture')
    return ingredient
    