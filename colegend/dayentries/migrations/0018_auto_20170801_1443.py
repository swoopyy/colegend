# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 12:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dayentries', '0017_auto_20170731_1131'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dayentry',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='dayentry',
            name='journal',
        ),
        migrations.RemoveField(
            model_name='dayentry',
            name='tags',
        ),
        migrations.DeleteModel(
            name='DayEntry',
        ),
    ]
