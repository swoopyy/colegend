# Generated by Django 2.0.3 on 2018-03-30 19:46

import colegend.core.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journey', '0018_hero_year_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='blueprint_day',
            field=colegend.core.fields.MarkdownField(blank=True),
        ),
        migrations.AddField(
            model_name='hero',
            name='blueprint_month',
            field=colegend.core.fields.MarkdownField(blank=True),
        ),
        migrations.AddField(
            model_name='hero',
            name='blueprint_week',
            field=colegend.core.fields.MarkdownField(blank=True),
        ),
        migrations.AddField(
            model_name='hero',
            name='roles',
            field=colegend.core.fields.MarkdownField(blank=True),
        ),
        migrations.AddField(
            model_name='hero',
            name='strategy',
            field=colegend.core.fields.MarkdownField(blank=True),
        ),
        migrations.AddField(
            model_name='hero',
            name='vision',
            field=colegend.core.fields.MarkdownField(blank=True),
        ),
    ]
