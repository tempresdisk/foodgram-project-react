from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet, mixins

from . import models
from . import serializers
from .filters import IngredientNameFilter
from .permissions import AuthPostRetrieve


class TagViewSet(ReadOnlyModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filterset_class = IngredientNameFilter


class RecipeViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    GenericViewSet):
    queryset = models.Recipe.objects.all()
    permission_classes = [AuthPostRetrieve]
    # filterset_class =

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.RecipeReadSerializer
        return serializers.RecipeWriteSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
