import pytest
from django.apps import apps as django_apps


@pytest.fixture
def tag():
    Tag = django_apps.get_model('api.Tag', require_ready=True)
    Tag.objects.create(
        name='tag_fixture', slug='tag-slug', color='#00ff00'
    )
    tag = Tag.objects.get(name='tag_fixture')
    return tag
    