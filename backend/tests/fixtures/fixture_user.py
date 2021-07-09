import pytest


@pytest.fixture
def admin(django_user_model):
    django_user_model.objects.create_superuser(
        username='TestUser', email='admin@foodgram.fake', password='1234567'
    )
    admin = django_user_model.objects.get(username='TestUser')
    admin.first_name = 'Test'
    admin.last_name = 'User'
    admin.save()
    return admin


@pytest.fixture
def token(admin):
    from djoser import utils
    from djoser.conf import settings

    token, _ = settings.TOKEN_MODEL.objects.get_or_create(user=admin)
    token_serializer_class = settings.SERIALIZERS.token

    return token_serializer_class(token).data


@pytest.fixture
def user_client(token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token["auth_token"]}')
    return client
