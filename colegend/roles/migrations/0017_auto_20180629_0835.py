# Generated by Django 2.0.4 on 2018-06-29 06:35

import colegend.core.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0016_auto_20180629_0018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='domains',
            new_name='powers',
        ),
        migrations.RenameField(
            model_name='role',
            old_name='accountabilities',
            new_name='services',
        ),
    ]
