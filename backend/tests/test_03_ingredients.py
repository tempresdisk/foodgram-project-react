import pytest


class Test03IngredientAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_ingredients_not_auth(self, client):
        response = client.get('/api/ingredients/')
        assert response.status_code != 404, (
            'Страница `/api/ingredients/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/ingredients/` без токена авторизации возвращается статус 200'
        )
        response = client.post('/api/ingredients/', data={})
        assert response.status_code == 405, (
            'Проверьте, что при POST запросе `/api/ingredients/` возвращается статус 405'
        )
