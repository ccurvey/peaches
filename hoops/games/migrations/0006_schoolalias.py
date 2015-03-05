# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_school_mascot'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(max_length=100)),
                ('school', models.ForeignKey(to='games.School')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
