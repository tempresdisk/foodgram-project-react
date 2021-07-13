import pytest

from .common import auth_client


class Test05RecipeAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_recipes_post_get_urls_status(self, client):
        response = client.get('/api/recipes/')
        assert response.status_code != 404, (
            'Страница `/api/recipes/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/recipes/` без токена авторизации возвращается статус 200'
        )
        response = client.post('/api/recipes/', data={})
        assert response.status_code == 401, (
            'Проверьте, что при POST запросе `/api/recipes/` без токена авторизации возвращается статус 401'
        )

    def create_recipe(self, user, ingredient_1, ingredient_2, tag):
        data = {
            'ingredients': [
                {'id': ingredient_1.id, 'amount': 100},
                {'id': ingredient_2.id, 'amount': 1}
            ],
            'tags': [tag.id],
            'image': (b'\x47\x49\x46\x38\x39\x61\x02\x00'
                      b'\x01\x00\x80\x00\x00\x00\x00\x00'
                      b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                      b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                      b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                      b'\x0A\x00\x3B'),
            'name': 'Test recipe',
            'text': 'test recipe text',
            'cooking_time': 3,
        }
        response = auth_client(user).post('/api/recipes/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/recipes/` авторизованным пользователем '
            'с правильными данными, возвращается статус 201'
        )


    @pytest.mark.django_db(transaction=True)
    def test_02_recipes_response_fields(self, client, test_user, vodka, pickle, tag):
        self.create_recipe(test_user, vodka, pickle, tag)
        response = client.get('/api/recipes/')
        response_data = response.json().get('results')[0]
        assert response_data.get('id') == test_user.recipe.id, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете `id`.'
        )
        assert response_data.get('tags')[0]['id'] == tag.id, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете `tags`.'
        )
        assert type(response_data.get('tags')) == list, (
            'Проверьте, что тип данных `tags` - массив'
        )
        assert response_data.get('author')['id'] == test_user.id, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете `author`.'
        )
        assert type(response_data.get('author')) == dict, (
            'Проверьте, что тип данных `author` - словарь'
        )
        assert response_data.get('ingredients')[0]['id'] == vodka.id, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете `ingredients`.'
        )
        assert type(response_data.get('ingredients')) == list, (
            'Проверьте, что тип данных `ingredients` - массив'
        )
        assert len(response_data.get('ingredients')) == 2, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете все ингредиенты рецепта.'
        )
        assert response_data.get('is_favorited') == False, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете `is_favorited`.'
        )
        assert response_data.get('is_in_shopping_cart') == False, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете `is_in_shopping_cart`.'
        )
        assert response_data.get('name') == test_user.recipe.first().name, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете `name`.'
        )
        assert response_data.get('image') == test_user.recipe.first().image, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете `image`.'
        )
        assert response_data.get('text') == test_user.recipe.first().text, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете `text`.'
        )
        assert response_data.get('cooking_time') == test_user.recipe.first().cooking_time, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете `cooking_time`.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_recipes_get_pagination(self, client):
        response = client.get('api/recipes/')
        data = response.json()
        assert 'count' in data, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете данные с пагинацией. '
            'Не найден параметр `count`'
        )
        assert 'next' in data, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете данные с пагинацией. '
            'Не найден параметр `next`'
        )
        assert 'previous' in data, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете данные с пагинацией. '
            'Не найден параметр `previous`'
        )
        assert 'results' in data, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете данные с пагинацией. '
            'Не найден параметр `results`'
        )
        assert data['count'] == 1, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете данные с пагинацией. '
            'Значение параметра `count` не правильное'
        )
        assert type(data['results']) == list, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете данные с пагинацией. '
            'Тип параметра `results` должен быть список'
        )
