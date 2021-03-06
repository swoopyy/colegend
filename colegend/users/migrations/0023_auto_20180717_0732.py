# Generated by Django 2.0.4 on 2018-07-17 05:32

import colegend.core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('checkpoints', '0002_auto_20160118_2151'),
        ('users', '0022_auto_20180707_0023'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCheckpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('checkpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkpoints.Checkpoint')),
            ],
            options={
                'abstract': False,
            },
            bases=(colegend.core.models.OwnedCheckMixin, models.Model),
        ),
        migrations.RemoveField(
            model_name='user',
            name='checkpoints',
        ),
        migrations.AddField(
            model_name='user',
            name='checkpoints',
            field=models.ManyToManyField(blank=True, related_name='users', through='users.UserCheckpoint', to='checkpoints.Checkpoint'),
        ),
        migrations.AddField(
            model_name='usercheckpoint',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
