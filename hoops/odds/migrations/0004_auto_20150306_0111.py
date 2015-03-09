# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('odds', '0003_auto_20150226_0145'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HalfSide',
        ),
        migrations.DeleteModel(
            name='HalfTotal',
        ),
        migrations.AlterField(
            model_name='proposition',
            name='value',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
