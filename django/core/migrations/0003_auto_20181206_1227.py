# Generated by Django 2.1.3 on 2018-12-06 12:27

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("socialaccount", "0003_extra_data_default_dict"),
        ("core", "0002_auto_20181205_2102"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiscordGuildMembership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "data",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, null=True
                    ),
                ),
                ("cached_date", models.DateTimeField(auto_now_add=True)),
                (
                    "guild",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.DiscordGuild",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        limit_choices_to={"provider": "discord"},
                        on_delete=django.db.models.deletion.CASCADE,
                        to="socialaccount.SocialAccount",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="discordguild",
            name="members",
            field=models.ManyToManyField(
                through="core.DiscordGuildMembership", to="socialaccount.SocialAccount"
            ),
        ),
    ]
