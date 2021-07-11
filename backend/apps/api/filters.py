from django_filters import CharFilter, FilterSet, NumberFilter
from django_filters.filters import BooleanFilter

from .models import Ingredient


class IngredientNameFilter(FilterSet):
    name = CharFilter(field_name='name', method='name_starts_with')

    class Meta:
        model = Ingredient
        fields = ('name',)

    def name_starts_with(self, queryset, slug, name):
        return queryset.filter(name__startswith=name)
