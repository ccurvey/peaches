# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guess', '0002_auto_20150312_0120'),
    ]

    operations = [
        migrations.CreateModel(
            name='OverWager',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('guess.totalwager',),
        ),
        migrations.CreateModel(
            name='UnderWager',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('guess.totalwager',),
        ),
    ]
