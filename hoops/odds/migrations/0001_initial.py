# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_schoolalias'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('spread', models.FloatField(null=True, blank=True)),
                ('total', models.FloatField(null=True, blank=True)),
                ('money_line', models.IntegerField(null=True, blank=True)),
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
            name='PointsPerPosession',
            fields=[
                ('predictionmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='odds.PredictionModel')),
            ],
            options={
            },
            bases=('odds.predictionmodel',),
        ),
        migrations.CreateModel(
            name='ReturnToMean',
            fields=[
                ('predictionmodel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='odds.PredictionModel')),
            ],
            options={
            },
            bases=('odds.predictionmodel',),
        ),
        migrations.AddField(
            model_name='prediction',
            name='model',
            field=models.ForeignKey(to='odds.PredictionModel'),
            preserve_default=True,
        ),
    ]
