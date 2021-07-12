from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'tags', views.TagViewSet, basename='tags')
router.register(r'ingredients', views.IngredientViewSet, basename='ingredients')
router.register('subscriptions/', views.SubscriptionViewSet, basename='subscription')
router.register(r'users/(?P<id>\d+)/subscribe/', views.SubscriptionViewSet, basename='subscribe')


urlpatterns = [
    path('', include(router.urls)),
]
