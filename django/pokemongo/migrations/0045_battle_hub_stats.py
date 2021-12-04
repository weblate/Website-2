# Generated by Django 2.2.17 on 2020-11-27 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pokemongo", "0044_add_gen6_badge"),
    ]

    operations = [
        migrations.AddField(
            model_name="update",
            name="battle_hub_stats_battles",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="PVP Battles. Can be found in the Battle Hub.",
                null=True,
                verbose_name="GO Battle League: Battles",
            ),
        ),
        migrations.AddField(
            model_name="update",
            name="battle_hub_stats_stardust",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="PVP Stardust Earned. Can be found in the Battle Hub.",
                null=True,
                verbose_name="GO Battle League: Stardust Earned",
            ),
        ),
        migrations.AddField(
            model_name="update",
            name="battle_hub_stats_streak",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="PVP Longest Streak. Can be found in the Battle Hub.",
                null=True,
                verbose_name="GO Battle League: Longest Streak",
            ),
        ),
        migrations.AddField(
            model_name="update",
            name="battle_hub_stats_wins",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="PVP Wins. Can be found in the Battle Hub.",
                null=True,
                verbose_name="GO Battle League: Wins",
            ),
        ),
    ]
