# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-06 09:12
from __future__ import unicode_literals

import colegend.core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(verbose_name='date')),
                ('amount', models.DecimalField(decimal_places=2, help_text='¤', max_digits=6, verbose_name='amount')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_related_name': 'donations',
                'verbose_name': 'donation',
                'verbose_name_plural': 'donations',
            },
            bases=(colegend.core.models.AutoUrlsMixin, colegend.core.models.OwnedCheckMixin, models.Model),
        ),
    ]
