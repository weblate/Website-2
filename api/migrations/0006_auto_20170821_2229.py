# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 22:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20170821_2157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trainers',
            old_name='discord_id',
            new_name='discord',
        ),
    ]
