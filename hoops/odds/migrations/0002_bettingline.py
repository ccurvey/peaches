# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0007_auto_20150225_0255'),
        ('odds', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BettingLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('line_type', models.CharField(max_length=1, choices=[(b'S', b'Spread'), (b'T', b'Total'), (b'M', b'Money')])),
                ('odds', models.FloatField()),
                ('game', models.ForeignKey(to='games.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
