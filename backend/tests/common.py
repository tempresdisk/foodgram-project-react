from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from djoser.conf import settings


def create_users_api(user_client):
    data = {
        'first_name': 'fsdfsdf',
        'last_name': 'dsgdsfg',
        'username': 'TestUser2342',
        'email': 'testuser2342@foodgram.fake',
        'password': 'ntcngfhjkm'
    }
    user_client.post('/api/users/', data=data)
    user = get_user_model().objects.get(username=data['username'])
    return user


def auth_client(user):
    token, _ = settings.TOKEN_MODEL.objects.get_or_create(user=user)
    token_serializer_class = settings.SERIALIZERS.token
    token = token_serializer_class(token).data
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token["auth_token"]}')
    return client
