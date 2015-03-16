# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('odds', '__first__'),
        ('games', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('money_line', models.IntegerField(null=True, blank=True)),
                ('_game_date', models.DateField(null=True, db_column=b'game_date', blank=True)),
                ('_opponent', models.ForeignKey(related_name='+', db_column=b'opponent_id', blank=True, to='games.Team', null=True)),
                ('_team', models.ForeignKey(db_column=b'team_id', blank=True, to='games.Team', null=True)),
                ('game', models.ForeignKey(to='games.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PredictionModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Wager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_name', models.CharField(max_length=100)),
                ('predicted_value', models.FloatField()),
                ('outcome', models.IntegerField(null=True, blank=True)),
                ('proposition', models.ForeignKey(to='odds.Proposition')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='prediction',
            name='model',
            field=models.ForeignKey(to='guess.PredictionModel'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='PointsPerPosession',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('guess.predictionmodel',),
        ),
        migrations.CreateModel(
            name='ReturnToMean',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('guess.predictionmodel',),
        ),
    ]
