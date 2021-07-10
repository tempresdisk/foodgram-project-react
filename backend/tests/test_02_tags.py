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
'''
    @pytest.mark.django_db(transaction=True)
    def test_02_tags_get(self, client, tag):
        response = client.get('/api/tags/')
        response_data = response.json()
        assert response_data.get('name') == tag.id, (
            'Проверьте, что при GET запросе `/api/tags/` возвращаете `id`.'
        )
        assert response_data.get('name') == tag.name, (
            'Проверьте, что при GET запросе `/api/tags/` возвращаете `name`.'
        )
        assert response_data.get('color') == tag.color, (
            'Проверьте, что при GET запросе `/api/tags/` возвращаете `color`.'
        )
        assert response_data.get('slug') == tag.slug, (
            'Проверьте, что при GET запросе `/api/tags/` возвращаете `color`.'
        )
        response = client.post('/api/tags/', data={})
        assert response.status_code == 405, (
            'Проверьте, что при POST запросе `/api/tags/` возвращается статус 405'
        )
'''
