# Generated by Django 2.0.3 on 2018-04-25 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_auto_20180425_0010'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='routine',
            options={'ordering': ('order',)},
        ),
        migrations.AlterUniqueTogether(
            name='routinehabit',
            unique_together={('routine', 'habit')},
        ),
    ]
