# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-24 19:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outcomes', '0003_auto_20160524_2056'),
    ]

    operations = [
        migrations.RenameField(
            model_name='outcome',
            old_name='time_estimate',
            new_name='estimate',
        ),
    ]