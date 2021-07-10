import pytest
from django.apps import apps as django_apps


@pytest.fixture
def Tag():
    Tag = django_apps.get_model('api.Tag', require_ready=True)
    return Tag


@pytest.fixture
def tag(Tag):
    Tag.objects.create(
        name='tag_fixture', slug='tag-slug', color='#00ff00'
    )
    tag = Tag.objects.get(name='tag_fixture')
    return tag
    