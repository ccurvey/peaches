# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('odds', '__first__'),
        ('guess', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SideWager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_name', models.CharField(max_length=100)),
                ('_outcome', models.IntegerField(null=True, db_column=b'outcome', blank=True)),
                ('proposition', models.ForeignKey(to='odds.Proposition')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TotalWager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_name', models.CharField(max_length=100)),
                ('over_under', models.CharField(max_length=1, choices=[(b'O', b'Over'), (b'U', b'Under')])),
                ('_outcome', models.IntegerField(null=True, db_column=b'outcome', blank=True)),
                ('proposition', models.ForeignKey(to='odds.Proposition')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='wager',
            name='proposition',
        ),
        migrations.DeleteModel(
            name='Wager',
        ),
        migrations.CreateModel(
            name='MoneyLineWager',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('guess.sidewager',),
        ),
    ]
