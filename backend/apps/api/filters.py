from django_filters import CharFilter, FilterSet

from .models import Ingredient, Recipe


class IngredientNameFilter(FilterSet):
    name = CharFilter(field_name='name', method='name_starts_with')

    class Meta:
        model = Ingredient
        fields = ('name',)

    def name_starts_with(self, queryset, slug, name):
        return queryset.filter(name__startswith=name)


class TagFilter(FilterSet):
    tags = CharFilter(field_name='tags__slug', method='filter_tags')

    def filter_tags(self, queryset, slug, tags):
        tags = self.request.query_params.getlist('tags')
        return queryset.filter(
            tags__slug__in=tags
        ).distinct()

    class Meta:
        model = Recipe
        fields = ('tags',)
