from django.urls import path, include
from djoser.views import TokenCreateView, TokenDestroyView

urlpatterns = [
    path('auth/token/login/', TokenCreateView.as_view(), name='token_obtain'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='token_destroy'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
