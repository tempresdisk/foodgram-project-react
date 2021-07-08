from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=False,
        help_text=_('Required. 30 characters or fewer.')
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=False,
        help_text=_('Required. 150 characters or fewer.')
    )
    email = models.EmailField(
        _('email address'),
        blank=False,
        help_text=_('Required.')
    )
