# Generated by Django 2.0.3 on 2018-04-16 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0011_book_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='rating',
            field=models.FloatField(blank=True, null=True, verbose_name='rating'),
        ),
    ]
