import pytest


class Test02TagAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_tags_not_auth(self, client):
        response = client.get('/api/tags/')
        assert response.status_code != 404, (
            'Страница `/api/tags/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/tags/` без токена авторизации возвращается статус 200'
        )
        response = client.post('/api/tags/', data={})
        assert response.status_code == 405, (
            'Проверьте, что при POST запросе `/api/tags/` возвращается статус 405'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_tags_get(self, client, tag):
        response = client.get(f'/api/tags/{tag.id}/')
        response_data = response.json()
        assert response_data.get('id') == tag.id, (
            'Проверьте, что при GET запросе `/api/tags/{id}/` возвращаете `id`.'
        )
        assert response_data.get('name') == tag.name, (
            'Проверьте, что при GET запросе `/api/tags/{id}/` возвращаете `name`.'
        )
        assert response_data.get('color') == tag.color, (
            'Проверьте, что при GET запросе `/api/tags/{id}/` возвращаете `color`.'
        )
        assert response_data.get('slug') == tag.slug, (
            'Проверьте, что при GET запросе `/api/tags/{id}/` возвращаете `slug`.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_tags_get_pagination(self, client):
        response = client.get(f'/api/tags/')
        data = response.json()
        assert 'count' not in data, (
            'Проверьте, что при GET запросе `/api/tags/` возвращаете данные без пагинации. '
            'Найден параметр `count`'
        )
        assert 'next' not in data, (
            'Проверьте, что при GET запросе `/api/tags/` возвращаете данные без пагинации. '
            'Найден параметр `next`'
        )
        assert 'previous' not in data, (
            'Проверьте, что при GET запросе `/api/tags/` возвращаете данные без пагинации. '
            'Найден параметр `previous`'
        )
        assert 'results' not in data, (
            'Проверьте, что при GET запросе `/api/tags/` возвращаете данные без пагинации. '
            'Найден параметр `results`'
        )
