import pytest
from django.contrib.auth import get_user_model

from .common import auth_client, create_users_api


class Test01UserAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_users_not_auth(self, client):
        response = client.get('/api/users/')

        assert response.status_code != 404, (
            'Страница `/api/users/` не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/users/` без токена авторизации возвращается статус 401'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_users_id_not_auth(self, client, admin):
        response = client.get(f'/api/users/{admin.id}/')

        assert response.status_code != 404, (
            'Страница `/api/users/{id}/` не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/users/{id}/` без токена авторизации возвращается статус 401'
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
    def test_04_users_post_login(self, client, admin):
        data = {
            'username': admin.username,
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
    def test_05_users_post_logout(self, user_client):
        response = user_client.post('/api/auth/token/logout/')
        assert response.status_code != 404, (
            'Страница `/api/auth/token/logout/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 204, (
            'Проверьте, что при POST запросе `/api/auth/token/logout/`авторизованного пользователя возвращается статус 204'
        )

    @pytest.mark.django_db(transaction=True)
    def test_06_users_id_get_auth(self, user_client, admin):
        #user, moderator = create_users_api(user_client)
        response = user_client.get(f'/api/users/{admin.id}/')
        assert response.status_code != 404, (
            'Страница `/api/users/{id}/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/{id}/` с токеном авторизации возвращается статус 200'
        )
        response_data = response.json()
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
    
    @pytest.mark.django_db(transaction=True)
    def test_07_users_username_patch_auth(self, user_client, admin):
        user, moderator = create_users_api(user_client)
        data = {
            'first_name': 'Admin',
            'last_name': 'Test',
            'bio': 'description'
        }
        response = user_client.patch(f'/api/users/{admin.username}/', data=data)
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/users/{username}/` '
            'с токеном авторизации возвращается статус 200'
        )
        test_admin = get_user_model().objects.get(username=admin.username)
        assert test_admin.first_name == data['first_name'], (
            'Проверьте, что при PATCH запросе `/api/users/{username}/` изменяете данные.'
        )
        assert test_admin.last_name == data['last_name'], (
            'Проверьте, что при PATCH запросе `/api/users/{username}/` изменяете данные.'
        )
        response = user_client.patch(f'/api/users/{user.username}/', data={'role': 'admin'})
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/users/{username}/` '
            'с токеном авторизации возвращается статус 200'
        )
        client_user = auth_client(user)
        response = client_user.get(f'/api/users/{admin.username}/')
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/users/{username}/` можно изменить роль пользователя'
        )

    @pytest.mark.django_db(transaction=True)
    def test_08_users_username_delete_auth(self, user_client):
        user, moderator = create_users_api(user_client)
        response = user_client.delete(f'/api/users/{user.username}/')
        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/api/users/{username}/` возвращаете статус 204'
        )
        assert get_user_model().objects.count() == 2, (
            'Проверьте, что при DELETE запросе `/api/users/{username}/` удаляете пользователя'
        )

    def check_permissions(self, user, user_name, admin):
        client_user = auth_client(user)
        response = client_user.get('/api/users/')
        assert response.status_code == 403, (
            f'Проверьте, что при GET запросе `/api/users/` '
            f'с токеном авторизации {user_name} возвращается статус 403'
        )
        data = {
            'username': 'TestUser9876',
            'role': 'user',
            'email': 'testuser9876@yamdb.fake'
        }
        response = client_user.post('/api/users/', data=data)
        assert response.status_code == 403, (
            f'Проверьте, что при POST запросе `/api/users/` '
            f'с токеном авторизации {user_name} возвращается статус 403'
        )

        response = client_user.get(f'/api/users/{admin.username}/')
        assert response.status_code == 403, (
            f'Проверьте, что при GET запросе `/api/users/{{username}}/` '
            f'с токеном авторизации {user_name} возвращается статус 403'
        )
        data = {
            'first_name': 'Admin',
            'last_name': 'Test',
            'bio': 'description'
        }
        response = client_user.patch(f'/api/users/{admin.username}/', data=data)
        assert response.status_code == 403, (
            f'Проверьте, что при PATCH запросе `/api/users/{{username}}/` '
            f'с токеном авторизации {user_name} возвращается статус 403'
        )
        response = client_user.delete(f'/api/users/{admin.username}/')
        assert response.status_code == 403, (
            f'Проверьте, что при DELETE запросе `/api/users/{{username}}/` '
            f'с токеном авторизации {user_name} возвращается статус 403'
        )

    @pytest.mark.django_db(transaction=True)
    def test_09_users_check_permissions(self, user_client, admin):
        user, moderator = create_users_api(user_client)
        self.check_permissions(user, 'обычного пользователя', admin)
        self.check_permissions(moderator, 'модератора', admin)

    @pytest.mark.django_db(transaction=True)
    def test_10_users_me_get(self, user_client, admin):
        user, moderator = create_users_api(user_client)
        response = user_client.get('/api/users/me/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/me/` с токеном авторизации возвращается статус 200'
        )
        response_data = response.json()
        assert response_data.get('username') == admin.username, (
            'Проверьте, что при GET запросе `/api/users/me/` возвращаете данные пользователя'
        )
        client_user = auth_client(moderator)
        response = client_user.get('/api/users/me/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/me/` с токеном авторизации возвращается статус 200'
        )
        response_data = response.json()
        assert response_data.get('username') == moderator.username, (
            'Проверьте, что при GET запросе `/api/users/me/` возвращаете данные пользователя'
        )
        assert response_data.get('role') == 'moderator', (
            'Проверьте, что при GET запросе `/api/users/me/` возвращаете данные пользователя'
        )
        assert response_data.get('email') == moderator.email, (
            'Проверьте, что при GET запросе `/api/users/me/` возвращаете данные пользователя'
        )
        response = client_user.delete('/api/users/me/')
        assert response.status_code == 405, (
            'Проверьте, что при DELETE запросе `/api/users/me/` возвращается статус 405'
        )

    @pytest.mark.django_db(transaction=True)
    def test_11_users_me_patch(self, user_client):
        user, moderator = create_users_api(user_client)
        data = {
            'first_name': 'Admin',
            'last_name': 'Test',
            'bio': 'description'
        }
        response = user_client.patch('/api/users/me/', data=data)
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/users/me/` с токеном авторизации возвращается статус 200'
        )
        response_data = response.json()
        assert response_data.get('bio') == 'description', (
            'Проверьте, что при PATCH запросе `/api/users/me/` изменяете данные'
        )
        client_user = auth_client(moderator)
        response = client_user.patch('/api/users/me/', data={'first_name': 'NewTest'})
        test_moderator = get_user_model().objects.get(username=moderator.username)
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/users/me/` с токеном авторизации возвращается статус 200'
        )
        assert test_moderator.first_name == 'NewTest', (
            'Проверьте, что при PATCH запросе `/api/users/me/` изменяете данные'
        )
