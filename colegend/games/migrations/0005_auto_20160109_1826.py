# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('games', '0004_auto_20160109_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='checkpoints',
        ),
        migrations.DeleteModel(
            name='Checkpoint',
        ),
    ]
