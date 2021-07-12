import pytest


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
        