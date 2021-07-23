import pytest
from django.contrib.auth import get_user_model
from rest_framework import test
from rest_framework.test import APIClient

from .common import auth_client, create_users_api


class Test01UserAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_users_not_auth(self, client):
        response = client.get('/api/users/')

        assert response.status_code != 404, (
            'Страница `/api/users/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/` без токена авторизации возвращается статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_users_id_not_auth(self, client, user_client, admin):
        response = client.get(f'/api/users/{admin.id}/')
        assert response.status_code != 404, (
            'Страница `/api/users/{id}/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/users/{id}/` без токена авторизации возвращается статус 401'
        )
        response = user_client.get(f'/api/users/{admin.id}/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/{id}/` авторизованным пользователемё возвращается статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_users_me_not_auth(self, client):
        response = client.get('/api/users/me/')

        assert response.status_code != 404, (
            'Страница `/api/users/me/` не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/users/me/` без токена авторизации возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_users_set_password(self, client, admin):
        response = client.get('/api/users/set_password/')

        assert response.status_code != 404, (
            'Страница `/api/users/set_password/` не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/users/set_password/` без токена авторизации возвращается статус 401'
        )
        data = {
            'current_password': '1234567',
            'new_password': 'new_1234567'
        }
        response = auth_client(admin).post('/api/users/set_password/', data=data)
        assert response.status_code == 302, (
            'Проверьте, что при POST запросе `/api/users/set_password` с правильными данными возвращается статус 302'
        )
        response = auth_client(admin).post('/api/users/set_password/', data={})
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/users/set_password` с неправильными данными возвращается статус 400'
        )

    @pytest.mark.django_db(transaction=True)
    def test_05_users_post_login(self, client, admin):
        data = {
            'email': admin.email,
            'password': '1234567'
        }
        response = client.post('/api/auth/token/login/', data=data)
        assert response.status_code != 404, (
            'Страница `/api/auth/token/login/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при POST запросе `/api/auth/token/login/` с правильными данными возвращается статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_06_users_post_logout(self, user_client):
        response = user_client.post('/api/auth/token/logout/')
        assert response.status_code != 404, (
            'Страница `/api/auth/token/logout/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 204, (
            'Проверьте, что при POST запросе `/api/auth/token/logout/`авторизованного пользователя возвращается статус 204'
        )

    @pytest.mark.django_db(transaction=True)
    def test_07_users_id_get_auth(self, user_client, admin):
        response = user_client.get(f'/api/users/{admin.id}/')
        assert response.status_code != 404, (
            'Страница `/api/users/{id}/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/{id}/` с токеном авторизации возвращается статус 200'
        )
        response_data = response.json()
        assert response_data.get('id') == admin.id, (
            'Проверьте, что при GET запросе `/api/users/{id}/` возвращаете `id`.'
        )
        assert response_data.get('username') == admin.username, (
            'Проверьте, что при GET запросе `/api/users/{id}/` возвращаете `username`.'
        )
        assert response_data.get('email') == admin.email, (
            'Проверьте, что при GET запросе `/api/users/{id}/` возвращаете `email`.'
        )
        assert response_data.get('first_name') == admin.first_name, (
            'Проверьте, что при GET запросе `/api/users/{id}` возвращаете `first_name`.'
        )
        assert response_data.get('last_name') == admin.last_name, (
            'Проверьте, что при GET запросе `/api/users/{id}` возвращаете `last_name`.'
        )
        assert response_data.get('is_subscribed') == False, (
            'Проверьте, что при GET запросе `/api/users/{id}` возвращаете `is_subscribed`.'
        )
        assert response_data.get('password') == None, (
            'Проверьте, что при GET запросе `/api/users/{id}` не возвращаете `password`.'
        )
    
    def check_permissions(self, user, user_name, admin):
        client_user = auth_client(user)
        response = client_user.get('/api/users/')
        assert response.status_code == 200, (
            f'Проверьте, что при GET запросе `/api/users/` '
            f'с токеном авторизации {user_name} возвращается статус 200'
        )
        data = {
            'username': 'TestUser9876',
            'password': 'gjkmpjdfntkm',
            'email': 'testuser9876@foodgram.fake',
            'first_name': 'Test',
            'last_name': 'User9876'
        }
        response = APIClient().post('/api/users/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/users/` '
            'неавторизованным пользователем возвращается статус 201'
        )
        testuser = get_user_model().objects.get(username='TestUser9876')
        testuser.delete()

    @pytest.mark.django_db(transaction=True)
    def test_08_users_check_permissions(self, user_client, admin):
        user = create_users_api(user_client)
        self.check_permissions(user, 'обычного пользователя', admin)
        self.check_permissions(admin, 'администратора', admin)

    @pytest.mark.django_db(transaction=True)
    def test_09_users_me_get(self, user_client, admin):
        user = create_users_api(user_client)
        response = user_client.get('/api/users/me/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/me/` с токеном авторизации возвращается статус 200'
        )
        response_data = response.json()
        assert response_data.get('username') == admin.username, (
            'Проверьте, что при GET запросе `/api/users/me/` возвращаете данные пользователя'
        )
        client_user = auth_client(user)
        response = client_user.get('/api/users/me/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/me/` с токеном авторизации возвращается статус 200'
        )
        response_data = response.json()
        assert response_data.get('id') == user.id, (
            'Проверьте, что при GET запросе `/api/users/me/` возвращаете `id`.'
        )
        assert response_data.get('username') == user.username, (
            'Проверьте, что при GET запросе `/api/users/me/` возвращаете `username`.'
        )
        assert response_data.get('email') == user.email, (
            'Проверьте, что при GET запросе `/api/users/me/` возвращаете `email`.'
        )
        assert response_data.get('first_name') == user.first_name, (
            'Проверьте, что при GET запросе `/api/users/me/` возвращаете `first_name`.'
        )
        assert response_data.get('last_name') == user.last_name, (
            'Проверьте, что при GET запросе `/api/users/me/` возвращаете `last_name`.'
        )
        assert response_data.get('password') == None, (
            'Проверьте, что при GET запросе `/api/users/me/` не возвращаете `password`.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_10_users_get_pagination(self, client, admin):
        response = client.get('/api/users/')
        data = response.json()
        assert 'count' in data, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные с пагинацией. '
            'Не найден параметр `count`'
        )
        assert 'next' in data, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные с пагинацией. '
            'Не найден параметр `next`'
        )
        assert 'previous' in data, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные с пагинацией. '
            'Не найден параметр `previous`'
        )
        assert 'results' in data, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные с пагинацией. '
            'Не найден параметр `results`'
        )
        assert data['count'] == 1, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные с пагинацией. '
            'Значение параметра `count` не правильное'
        )
        assert type(data['results']) == list, (
            'Проверьте, что при GET запросе `/api/users/` возвращаете данные с пагинацией. '
            'Тип параметра `results` должен быть список'
        )
