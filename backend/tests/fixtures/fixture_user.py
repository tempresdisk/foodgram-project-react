import pytest


@pytest.fixture
def admin(django_user_model):
    django_user_model.objects.create_superuser(
        username='TestAdmin', email='admin@foodgram.fake', password='1234567'
    )
    admin = django_user_model.objects.get(username='TestAdmin')
    admin.first_name = 'Test'
    admin.last_name = 'Admin'
    admin.save()
    return admin

@pytest.fixture
def test_user(django_user_model):
    django_user_model.objects.create(
        username='TestUser', email='test_user@foodgram.fake', password='7654321',
        first_name='Test', last_name='User'
    )
    test_user = django_user_model.objects.get(username='TestUser')
    return test_user


@pytest.fixture
def token(admin):
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
