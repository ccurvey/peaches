# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20150223_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='assists',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='blocks',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='defensive_points_per_posession',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='field_goal_pct',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='fouls',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='free_throw_pct',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='game_date',
            field=models.DateField(default='1900-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='location',
            field=models.CharField(default='H', max_length=1, choices=[(b'H', b'Home'), (b'A', b'Away'), (b'N', b'Neutral')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='offensive_points_per_posession',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='offensive_rebounds',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='opponent',
            field=models.ForeignKey(related_name='+', default=0, to='games.Team'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='points_against',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='points_for',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='posessions',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='ppws',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='result',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'W', b'Won'), (b'L', b'Lost')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='steals',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='team',
            field=models.ForeignKey(default=0, to='games.Team'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='three_point_pct',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='to_r',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='total_rebounds',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='turnover_ratio',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
