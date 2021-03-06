# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-08 18:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outcomes', '0019_outcome_completed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='outcome',
            name='comparisons',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='sore comparisons'),
        ),
        migrations.AddField(
            model_name='outcome',
            name='score',
            field=models.PositiveSmallIntegerField(default=1000, verbose_name='score'),
        ),
    ]
