# Generated by Django 2.0.3 on 2018-04-24 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20180424_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AddField(
            model_name='habit',
            name='is_controlled',
            field=models.BooleanField(default=False, help_text='Designates whether this habit is controlled by the system.', verbose_name='active'),
        ),
    ]
