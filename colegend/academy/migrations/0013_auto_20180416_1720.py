# Generated by Django 2.0.3 on 2018-04-16 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0012_auto_20180416_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='rating',
            field=models.FloatField(default=0, verbose_name='rating'),
        ),
    ]
