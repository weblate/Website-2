# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-22 14:14
from __future__ import unicode_literals

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20170822_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='factions',
            name='faction_image',
            field=models.ImageField(blank=True, null=True, upload_to=api.models.factionImagePath),
        ),
        migrations.AddField(
            model_name='factions',
            name='leader_image',
            field=models.ImageField(blank=True, null=True, upload_to=api.models.leaderImagePath),
        ),
        migrations.AddField(
            model_name='trainer',
            name='faction',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='api.Factions'),
        ),
    ]
