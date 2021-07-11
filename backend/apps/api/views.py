from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from . import models
from . import serializers


class TagViewSet(ReadOnlyModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    #queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    #filterset_fields = ['name']
    #search_fields = ['^name']

    def get_queryset(self):
        ingredient_name = self.request.query_params['name']
        ingredients = models.Ingredient.objects.filter(name__startswith=ingredient_name)
        return ingredients
