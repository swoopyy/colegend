# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-08 19:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('outcomes', '0008_auto_20160602_1833'),
        ('dayentries', '0011_auto_20170208_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayentry',
            name='outcome_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='day_focus_2', to='outcomes.Outcome'),
        ),
        migrations.AddField(
            model_name='dayentry',
            name='outcome_3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='day_focus_3', to='outcomes.Outcome'),
        ),
        migrations.AddField(
            model_name='dayentry',
            name='outcome_4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='day_focus_4', to='outcomes.Outcome'),
        ),
        migrations.AlterField(
            model_name='dayentry',
            name='outcome_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='day_focus_1', to='outcomes.Outcome'),
        ),
    ]
