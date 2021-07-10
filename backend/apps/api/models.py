from django.db import models
from django.utils.translation import gettext_lazy as _

from .fields import fields


class Tag(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        unique=True,
        max_length=24
    )
    color = fields.ColorField(
        verbose_name=_('Цвет'),
        unique=True
    )
    slug = models.SlugField(
        verbose_name=_('Слаг'),
        unique=True
    )

    class Meta:
        app_label = 'api'
        verbose_name = _('Тэг')
        verbose_name_plural = _('Тэги')

    def __str__(self):
        return self.name
