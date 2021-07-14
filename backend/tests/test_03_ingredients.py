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

    @pytest.mark.django_db(transaction=True)
    def test_02_ingredients_get(self, client, vodka):
        response = client.get(f'/api/ingredients/{vodka.id}/')
        response_data = response.json()
        assert response_data.get('id') == vodka.id, (
            'Проверьте, что при GET запросе `/api/ingredients/{id}/` возвращаете `id`.'
        )
        assert response_data.get('name') == vodka.name, (
            'Проверьте, что при GET запросе `/api/ingredients/{id}/` возвращаете `name`.'
        )
        assert response_data.get('measurement_unit') == vodka.measurement_unit, (
            'Проверьте, что при GET запросе `/api/ingredients/{id}/` возвращаете `measurement_unit`.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_ingredients_get_pagination(self, client):
        response = client.get(f'/api/ingredients/')
        data = response.json()
        assert 'count' not in data, (
            'Проверьте, что при GET запросе `/api/ingredients/` возвращаете данные без пагинации. '
            'Найден параметр `count`'
        )
        assert 'next' not in data, (
            'Проверьте, что при GET запросе `/api/ingredients/` возвращаете данные без пагинации. '
            'Найден параметр `next`'
        )
        assert 'previous' not in data, (
            'Проверьте, что при GET запросе `/api/ingredients/` возвращаете данные без пагинации. '
            'Найден параметр `previous`'
        )
        assert 'results' not in data, (
            'Проверьте, что при GET запросе `/api/ingredients/` возвращаете данные без пагинации. '
            'Найден параметр `results`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_ingredients_get_filter(self, client, pickle):
        name_starts_with = pickle.name[:3]
        response = client.get(f'/api/ingredients/?name={name_starts_with}')
        response_data = response.json()
        assert response_data[0].get('name') == pickle.name, (
            'Проверьте, что при GET запросе `/api/ingredients/?name={query}` возвращается ожидаемый результат.'
        )
        