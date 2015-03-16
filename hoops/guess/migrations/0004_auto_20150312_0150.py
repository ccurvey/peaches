# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guess', '0003_overwager_underwager'),
    ]

    operations = [
        migrations.AddField(
            model_name='sidewager',
            name='predicted_value',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='totalwager',
            name='predicted_value',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
