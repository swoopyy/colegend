# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-08 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='name'),
        ),
    ]