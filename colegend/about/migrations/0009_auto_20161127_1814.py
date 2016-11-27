# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 17:14
from __future__ import unicode_literals

import colegend.cms.blocks
from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0008_aboutpage_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutpage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField((('heading', colegend.cms.blocks.HeadingBlock()), ('rich_text', colegend.cms.blocks.RichTextBlock()), ('image', colegend.cms.blocks.ImageBlock()), ('embed', colegend.cms.blocks.EmbedBlock()), ('html', wagtail.wagtailcore.blocks.RawHTMLBlock())), blank=True),
        ),
    ]
