# Generated by Django 2.0.4 on 2018-08-11 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outcomes', '0024_outcome_related_outcomes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outcome',
            name='inbox',
            field=models.BooleanField(default=False),
        ),
    ]
