# Generated by Django 2.1.4 on 2018-12-14 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pokemongo", "0017_auto_20181213_1025"),
        ("core", "0010_auto_20181214_1439"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="DiscordGuildChannel",
            new_name="DiscordChannel",
        ),
        migrations.RenameModel(
            old_name="DiscordGuildRole",
            new_name="DiscordRole",
        ),
    ]
