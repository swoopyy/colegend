# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-13 23:30
from __future__ import unicode_literals

import colegend.core.fields
import colegend.core.validators
import colegend.dayentries.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dayentries', '0015_auto_20170614_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayentry',
            name='date',
            field=colegend.core.fields.DateField(default=colegend.dayentries.models.get_today, validators=[colegend.core.validators.validate_date_today_tomorrow_or_past]),
        ),
    ]
