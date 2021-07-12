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
        