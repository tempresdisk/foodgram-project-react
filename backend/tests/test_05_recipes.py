import pytest

from .common import auth_client


class Test05RecipeAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_recipes_post_get_urls_status(self, client, tag, vodka, pickle,  test_user):
        response = client.get('/api/recipes/')
        assert response.status_code != 404, (
            'Страница `/api/recipes/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/recipes/` без токена авторизации возвращается статус 200'
        )
        data = {
            'tags': [tag.id],
            'image': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAyADIDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5rooor8DP9oAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD/2Q==',
            'name': 'Test recipe',
            'text': 'test recipe text',
            'cooking_time': 3,
            'ingredients':[
                {'id': vodka.id, 'amount': 100},
                {'id': pickle.id, 'amount': 1}
            ],
        }
        response = client.post('/api/recipes/', data=data, format='json')
        assert response.status_code == 401, (
            'Проверьте, что при POST запросе `/api/recipes/` без токена авторизации возвращается статус 401'
        )
        response = auth_client(test_user).post('/api/recipes/', data=data, format='json')
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/recipes/` авторизованным пользователем '
            'с правильными данными, возвращается статус 201'
        )

    def create_recipe(self, user, ingredient_1, ingredient_2, tag):
        data = {
            'ingredients': [
                {'id': ingredient_1.id, 'amount': 100},
                {'id': ingredient_2.id, 'amount': 1}
            ],
            'tags': [tag.id],
            'image': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAyADIDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5rooor8DP9oAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD/2Q==',
            'name': 'Test recipe',
            'text': 'test recipe text',
            'cooking_time': 3,
        }
        auth_client(user).post('/api/recipes/', data=data, format='json')

    @pytest.mark.django_db(transaction=True)
    def test_02_recipes_response_fields(self, client, test_user, vodka, pickle, tag):
        self.create_recipe(test_user, vodka, pickle, tag)
        response = client.get('/api/recipes/')
        response_data = response.json().get('results')[0]
        assert response_data.get('id') == test_user.recipes.first().id, (
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
        assert response_data.get('name') == test_user.recipes.first().name, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете `name`.'
        )
        assert test_user.recipes.first().image.url in response_data.get('image'), (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете `image`.'
        )
        assert response_data.get('text') == test_user.recipes.first().text, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете `text`.'
        )
        assert response_data.get('cooking_time') == test_user.recipes.first().cooking_time, (
            'Проверьте, что при GET запросе `/api/recipes/` возвращаете `cooking_time`.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_recipes_get_pagination(self, client, test_user, vodka, pickle, tag):
        self.create_recipe(test_user, vodka, pickle, tag)
        response = client.get('/api/recipes/')
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

    @pytest.mark.django_db(transaction=True)
    def test_04_recipes_put(self, client, user_client, test_user, vodka, pickle, tag):
        self.create_recipe(test_user, vodka, pickle, tag)
        data = {
            'ingredients': [
                {'id': vodka.id, 'amount': 1},
                {'id': pickle.id, 'amount': 100}
            ],
            'tags': [tag.id],
            'image': 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAAyADIDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5rooor8DP9oAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD/2Q==',
            'name': 'Test recipe',
            'text': 'test recipe text',
            'cooking_time': 5,
        }
        recipe_id = test_user.recipes.first().id
        response = client.put(f'/api/recipes/{recipe_id}/', data=data, format='json')
        assert response.status_code == 401, (
            'Проверьте, что при PUT запросе `/api/recipes/{id}/` неавторизованным пользователем '
            'с правильными данными, возвращается статус 401'
        )
        response = user_client.put(f'/api/recipes/{recipe_id}/', data=data, format='json')
        assert response.status_code == 403, (
            'Проверьте, что при PUT запросе `/api/recipes/{id}/` авторизованным пользователем, не являющегося автором рецепта, '
            'с правильными данными, возвращается статус 403'
        )
        response = auth_client(test_user).put(f'/api/recipes/{recipe_id}/', data=data, format='json')
        assert response.status_code == 200, (
            'Проверьте, что при PUT запросе `/api/recipes/{id}/` авторизованным пользователем, являющегося автором рецепта, '
            'с правильными данными, возвращается статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_05_recipes_delete(self, client, user_client, test_user, vodka, pickle, tag):
        self.create_recipe(test_user, vodka, pickle, tag)
        recipe_id = test_user.recipes.first().id
        response = client.delete(f'/api/recipes/{recipe_id}/')
        assert response.status_code != 404, (
            'Страница `/api/recipes/{id}` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 401, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/` неавторизованным пользователем возвращается статус 401'
        )
        response = user_client.delete(f'/api/recipes/{recipe_id}/')
        assert response.status_code == 403, (
            'Проверьте, что при DELETE запросе `/api/recipes/` авторизованным пользователем, не являющегося автором рецепта, возвращается статус 403'
        )
        response = auth_client(test_user).delete(f'/api/recipes/{recipe_id}/')
        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/` авторизованным пользователем, являющегося автором рецепта, возвращается статус 204'
        )

    @pytest.mark.django_db(transaction=True)
    def test_06_recipes_favorite(self, client, user_client, test_user, vodka, pickle, tag):  # `favorite`, that is how it is in redoc
        self.create_recipe(test_user, vodka, pickle, tag)
        recipe_id = test_user.recipes.first().id
        response = client.get(f'/api/recipes/{recipe_id}/favorite/')
        assert response.status_code != 404, (
            'Страница `/api/recipes/{id}/favorite/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/recipes/{id}/favorite/` неавторизованным пользователем, возвращается статус 401'
        )
        favorites_count = test_user.is_favorited.all().count()
        response = auth_client(test_user).get(f'/api/recipes/{recipe_id}/favorite/')
        assert response.status_code == 201, (
            'Проверьте, что при GET запросе `/api/recipes/{id}/favorite/` авторизованным пользователем, возвращается статус 201'
        )
        assert test_user.is_favorited.all().count() == favorites_count + 1, (
            'Проверьте, что при GET запросе `/api/recipes/{id}/favorite/` авторизованным пользователем, создаётся новая запись в базе данных'
        ) 
        response = auth_client(test_user).get(f'/api/recipes/{recipe_id}/favorite/')
        assert response.status_code == 400, (
            'Проверьте, что при GET запросе `/api/recipes/{id}/favorite/` тем же авторизованным пользователем, возвращается статус 400 '
            'Проверка уникальности избранный рецепт + пользователь'
        )
        response = client.delete(f'/api/recipes/{recipe_id}/favorite/')
        assert response.status_code == 401, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/favorite/` неавторизованным пользователем, возвращается статус 401'
        )
        response = user_client.delete(f'/api/recipes/{recipe_id}/favorite/')
        assert response.status_code == 400, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/favorite/` авторизованным пользователем {id} недобавленного в избранное рецепта, '
            'возвращается статус 400'
        )
        response = auth_client(test_user).delete(f'/api/recipes/{recipe_id}/favorite/')
        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/favorite/` авторизованным пользователем {id} добавленного в избранное рецепта, '
            'возвращается статус 204'
        )
        assert test_user.is_favorited.all().count() == favorites_count, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/favorite/` авторизованным пользователем {id} добавленного в избранное рецепта, '
            'удаляется соответствующая запись из базы данных'
        )

    @pytest.mark.django_db(transaction=True)
    def test_07_recipes_shopping_cart(self, client, user_client, test_user, vodka, pickle, tag):
        self.create_recipe(test_user, vodka, pickle, tag)
        recipe_id = test_user.recipes.first().id
        response = client.get(f'/api/recipes/{recipe_id}/shopping_cart/')
        assert response.status_code != 404, (
            'Страница `/api/recipes/{id}/shopping_cart/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/recipes/{id}/shopping_cart/` неавторизованным пользователем, возвращается статус 401'
        )
        shopping_cart_count = test_user.is_in_shopping_cart.all().count()
        response = auth_client(test_user).get(f'/api/recipes/{recipe_id}/shopping_cart/')
        assert response.status_code == 201, (
            'Проверьте, что при GET запросе `/api/recipes/{id}/shopping_cart/` авторизованным пользователем, возвращается статус 201'
        )
        assert test_user.is_in_shopping_cart.all().count() == shopping_cart_count + 1, (
            'Проверьте, что при GET запросе `/api/recipes/{id}/shopping_cart/` авторизованным пользователем, создаётся новая запись в базе данных'
        ) 
        response = auth_client(test_user).get(f'/api/recipes/{recipe_id}/shopping_cart/')
        assert response.status_code == 400, (
            'Проверьте, что при GET запросе `/api/recipes/{id}/shopping_cart/` тем же авторизованным пользователем, возвращается статус 400 '
            'Проверка уникальности рецепт в списках покупок + пользователь'
        )
        response = client.delete(f'/api/recipes/{recipe_id}/shopping_cart/')
        assert response.status_code == 401, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/shopping_cart/` неавторизованным пользователем, возвращается статус 401'
        )
        response = user_client.delete(f'/api/recipes/{recipe_id}/shopping_cart/')
        assert response.status_code == 400, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/shopping_cart/` авторизованным пользователем {id} недобавленного в избранное рецепта, '
            'возвращается статус 400'
        )
        response = auth_client(test_user).delete(f'/api/recipes/{recipe_id}/shopping_cart/')
        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/shopping_cart/` авторизованным пользователем {id} добавленного в избранное рецепта, '
            'возвращается статус 204'
        )
        assert test_user.is_in_shopping_cart.all().count() == shopping_cart_count, (
            'Проверьте, что при DELETE запросе `/api/recipes/{id}/shopping_cart/` авторизованным пользователем {id} добавленного в избранное рецепта, '
            'удаляется соответствующая запись из базы данных'
        )

    @pytest.mark.django_db(transaction=True)
    def test_08_recipes_download_shopping_cart(self, client, user_client):
        response = client.get(f'/api/recipes/download_shopping_cart/')
        assert response.status_code != 404, (
            'Страница `/api/recipes/download_shopping_cart/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 401, (
            'Проверьте, что при GET запросе `/api/recipes/download_shopping_cart/` неавторизованным пользователем, возвращается статус 401'
        )
        response = user_client.get(f'/api/recipes/download_shopping_cart/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/recipes/download_shopping_cart/` авторизованным пользователем, возвращается статус 200'
        )
        assert response['Content-Type'] == 'application/pdf', (
            'Проверьте, что GET запросе `/api/recipes/download_shopping_cart/` авторизованным пользователем, '
            'тип возвращаемого содержимого `application/pdf`'
        )
