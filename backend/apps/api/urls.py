from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'tags', views.TagViewSet, basename='tags')
router.register(r'ingredients', views.IngredientViewSet, basename='ingredients')
router.register(r'recipes', views.RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
]
