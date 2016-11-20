# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-20 22:02
from __future__ import unicode_literals

import colegend.core.fields
import colegend.core.validators
import datetime
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dayentries', '0007_auto_20160210_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayentry',
            name='date',
            field=colegend.core.fields.DateField(default=datetime.datetime.today, validators=[colegend.core.validators.validate_date_today_tomorrow_or_past]),
        ),
    ]
