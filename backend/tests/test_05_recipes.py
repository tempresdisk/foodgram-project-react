import pytest


class Test05RecipeAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_recipes_not_auth(self, client):
        response = client.get('/api/recipes/')
        assert response.status_code != 404, (
            'Страница `/api/recipes/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/recipes/` без токена авторизации возвращается статус 200'
        )