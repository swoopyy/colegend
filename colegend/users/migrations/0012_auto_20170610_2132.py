# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-10 19:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_auto_20170610_2131'),
        ('users', '0011_user_purpose'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='clan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='community.Clan', verbose_name='clan'),
        ),
        migrations.AddField(
            model_name='user',
            name='tribe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='community.Tribe', verbose_name='tribe'),
        ),
    ]