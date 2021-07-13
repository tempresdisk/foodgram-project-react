import pytest

from .common import auth_client


class Test04SubscriptionAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_subscriptions_auth(self, client, user_client):
        response = user_client.get('/api/users/subscriptions/')
        assert response.status_code != 404, (
            'Страница `/api/users/subscriptions/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/subscriptions/` авторизованным пользователем возвращается статус 200'
        )
        response = client.get('/api/users/subscriptions/')
        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/users/subscriptions/` без токена авторизации возвращается статус 401'
        )
        response = user_client.post('/api/users/subscriptions/', data={})
        assert response.status_code == 405, (
            'Проверьте, что при POST запросе `/api/users/subscriptions/` возвращается статус 405'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_subscriptions_pagination(self, user_client):
        response = user_client.get(f'/api/users/subscriptions/')
        data = response.json()
        assert 'count' in data, (
            'Проверьте, что при GET запросе `/api/users/subscriptions` возвращаете данные с пагинацией. '
            'Не найден параметр `count`'
        )
        assert 'next' in data, (
            'Проверьте, что при GET запросе `/api/users/subscriptions` возвращаете данные с пагинацией. '
            'Не найден параметр `next`'
        )
        assert 'previous' in data, (
            'Проверьте, что при GET запросе `/api/users/subscriptions` возвращаете данные с пагинацией. '
            'Не найден параметр `previous`'
        )
        assert 'results' in data, (
            'Проверьте, что при GET запросе `/api/users/subscriptions` возвращаете данные с пагинацией. '
            'Не найден параметр `results`'
        )
        assert data['count'] == 0, (
            'Проверьте, что при GET запросе `/api/users/subscriptions` возвращаете данные с пагинацией. '
            'Значение параметра `count` не правильное'
        )
        assert type(data['results']) == list, (
            'Проверьте, что при GET запросе `/api/users/subscriptions` возвращаете данные с пагинацией. '
            'Тип параметра `results` должен быть список'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_subscriptions_subscribe(self, client, user_client, admin, test_user):
        response = client.get(f'/api/users/{admin.id}/subscribe/')
        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/users/subscriptions/` без токена авторизации возвращается статус 401'
        )
        response = user_client.get(f'/api/users/{admin.id}/subscribe/')
        assert response.status_code != 404, (
            'Страница `/api/users/{id}/subscribe/` не найдена, проверьте этот адрес в *urls.py*'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_subscriptions_subscribe_logic(self, admin, test_user):
        first_client = auth_client(test_user)
        response = first_client.get(f'/api/users/42/subscribe/')
        assert response.status_code == 404, (
            'Проверьте, что при GET запросе `/api/users/{id}/subscribe/` авторизованным пользователем, '
            '(случай с несуществующим пользователем) возвращается статус 404'
        )
        response = first_client.get(f'/api/users/{test_user.id}/subscribe/')
        assert response.status_code == 403, (
            'Проверьте, что при GET запросе `/api/users/{id}/subscribe/` авторизованным пользователем, '
            '(случай с подпиской на себя) возвращается статус 403'
        )
        count_subscribed_on = admin.subscribed_on.all().count()
        response = first_client.get(f'/api/users/{admin.id}/subscribe/')
        assert response.status_code == 201, (
            'Проверьте, что при GET запросе `/api/users/{id}/subscribe/` авторизованным пользователем, '
            '(случай существующего автора, без подписки) возвращается статус 201'
        )
        assert test_user.subscribed_on.all().count() == count_subscribed_on + 1, (
            'Проверьте, что в случае возвращения статуса 201, создаётся запись в базе данных'
        )
        response = first_client.get(f'/api/users/{admin.id}/subscribe/')
        assert response.status_code == 403, (
            'Проверьте, что при GET запросе `/api/users/{id}/subscribe/` авторизованным пользователем, '
            '(случай повторной подписки) возвращается статус 403'
        )
        response = first_client.delete(f'/api/users/{test_user.id}/subscribe/')
        assert response.status_code == 400, (
            'Проверьте, что при GET запросе `/api/users/{id}/subscribe/` авторизованным пользователем, '
            '(случай отмены несуществующей подписки) возвращается статус 400'
        )
        response = first_client.delete(f'/api/users/{admin.id}/subscribe/')
        assert response.status_code == 204, (
            'Проверьте, что при GET запросе `/api/users/{id}/subscribe/` авторизованным пользователем, '
            '(случай отмены несуществующей подписки) возвращается статус 204'
        )
        assert test_user.subscribed_on.all().count() == count_subscribed_on, (
            'Проверьте, что в случае возвращения статуса 204, удаляется запись в базе данных'
        )

    def create_subscription(self, author, user):
        first_client = auth_client(user)
        first_client.get(f'/api/users/{author.id}/subscribe/')

    @pytest.mark.django_db(transaction=True)
    def test_05_subscriptions_response_fields(self, client, admin, test_user):
        count_subscribed_on = test_user.subscribed_on.all().count()
        self.create_subscription(admin, test_user)
        assert test_user.subscribed_on.all().count() == count_subscribed_on + 1
        response = auth_client(test_user).get(f'/api/users/subscriptions/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/users/subscriptions/` авторизованным пользователем возвращается статус 200'
        )
        response_data = response.json().get('results')[0]
        assert response_data.get('id') == admin.id, (
            'Проверьте, что при GET запросе `/api/users/subscriptions` возвращаете `id`.'
        )
        assert response_data.get('username') == admin.username, (
            'Проверьте, что при GET запросе `/api/users/subscriptions` возвращаете `username`.'
        )
        assert response_data.get('email') == admin.email, (
            'Проверьте, что при GET запросе `/api/users/subscriptions` возвращаете `email`.'
        )
        assert response_data.get('first_name') == admin.first_name, (
            'Проверьте, что при GET запросе `/api/users/subscriptions` возвращаете `first_name`.'
        )
        assert response_data.get('last_name') == admin.last_name, (
            'Проверьте, что при GET запросе `/api/users/subscriptions` возвращаете `last_name`.'
        )
        assert response_data.get('is_subscribed') == True, (
            'Проверьте, что при GET запросе `/api/users/subscriptions` возвращаете `is_subscribed`.'
        )
        assert response_data.get('recipes') == admin.recipes, (
            'Проверьте, что при GET запросе `/api/users/subscriptions` возвращаете `recipes`.'
        )
        assert response_data.get('recipes_count') == 0, (
            'Проверьте, что при GET запросе `/api/users/subscriptions` возвращаете `recipes_count`.'
        )
