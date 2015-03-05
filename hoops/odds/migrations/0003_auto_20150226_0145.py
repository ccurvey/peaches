# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0007_auto_20150225_0255'),
        ('odds', '0002_bettingline'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('class_name', models.CharField(max_length=100)),
                ('value', models.FloatField()),
                ('payoff', models.IntegerField(default=-110)),
                ('game', models.ForeignKey(to='games.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Wager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wager_amount', models.FloatField()),
                ('_payoff_amount', models.FloatField(null=True, db_column=b'payoff_amount', blank=True)),
                ('proposition', models.ForeignKey(to='odds.Proposition')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameMoney',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('odds.proposition',),
        ),
        migrations.CreateModel(
            name='GameSide',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('odds.proposition',),
        ),
        migrations.CreateModel(
            name='GameTotal',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('odds.proposition',),
        ),
        migrations.CreateModel(
            name='HalfSide',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('odds.proposition',),
        ),
        migrations.CreateModel(
            name='HalfTotal',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('odds.proposition',),
        ),
        migrations.AlterField(
            model_name='bettingline',
            name='odds',
            field=models.FloatField(default=-110),
            preserve_default=True,
        ),
    ]
