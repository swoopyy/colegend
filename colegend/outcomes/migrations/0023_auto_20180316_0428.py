# Generated by Django 2.0.3 on 2018-03-16 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outcomes', '0022_auto_20180313_1234'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='outcome',
            options={'ordering': ['-score'], 'verbose_name': 'outcome', 'verbose_name_plural': 'outcomes'},
        ),
    ]