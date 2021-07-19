from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet, mixins

from . import models
from . import serializers
from .filters import IngredientNameFilter, TagFilter
from .permissions import AuthPostRetrieve


class TagViewSet(ReadOnlyModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientReadSerializer
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
    #serializer_class = serializers.RecipeSerializer
    permission_classes = [AuthPostRetrieve]
    filterset_class = TagFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.RecipeReadSerializer
        return serializers.RecipeWriteSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        
        recipe = get_object_or_404(models.Recipe, pk=pk)
        user = request.user

        if request.method == 'GET':
            if not user.is_favorited.filter(recipe=recipe).exists():
                models.Favourite.objects.create(user=user, recipe=recipe)
                serializer = serializers.FavouriteSerializer(recipe, context={'request': request})
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            data = {
                "errors":"Этот рецепт уже есть в избранном"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_favorited.filter(recipe=recipe).exists():
            data = {
                "errors":"Этого рецепта не было в вашем избранном"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        models.Favourite.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        
        recipe = get_object_or_404(models.Recipe, pk=pk)
        user = request.user

        if request.method == 'GET':
            if not user.shopping_cart.filter(recipe=recipe).exists():
                models.ShoppingCart.objects.create(user=user, recipe=recipe)
                serializer = serializers.FavouriteSerializer(recipe, context={'request': request})
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            data = {
                "errors":"Этот рецепт уже есть в списке покупок"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        if not user.shopping_cart.filter(recipe=recipe).exists():
            data = {
                "errors":"Этого рецепта не было в вашем списке покупок"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        models.ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
