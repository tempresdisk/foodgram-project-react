# Generated by Django 3.0.5 on 2021-07-21 05:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20210721_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0, message='больше либо равно 0')]),
        ),
    ]
