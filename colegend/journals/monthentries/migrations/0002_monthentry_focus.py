# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-23 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monthentries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthentry',
            name='focus',
            field=models.TextField(blank=True),
        ),
    ]
