# Generated by Django 2.1.7 on 2019-10-03 14:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pokemongo", "0027_auto_20190520_1453"),
    ]

    operations = [
        migrations.RenameField(
            model_name="update",
            old_name="badge_pokedex_entries_unknown",
            new_name="badge_pokedex_entries_gen8",
        ),
        migrations.AddField(
            model_name="update",
            name="badge_photobombadge_rocket_grunts_defeated",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Defeat 1000 Team GO Rocket Grunts.",
                null=True,
                verbose_name="Hero",
            ),
        ),
        migrations.AddField(
            model_name="update",
            name="badge_pokedex_entries_gen5",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Register 100 Pokémon first discovered in the Unova region to the Pokédex.",
                null=True,
                validators=[django.core.validators.MaxValueValidator(156)],
                verbose_name="Unova",
            ),
        ),
        migrations.AddField(
            model_name="update",
            name="badge_pokedex_entries_gen6",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Register x Pokémon first discovered in the Kalos region to the Pokédex.",
                null=True,
                validators=[django.core.validators.MaxValueValidator(72)],
                verbose_name="Kalos",
            ),
        ),
        migrations.AddField(
            model_name="update",
            name="badge_pokedex_entries_gen7",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Register x Pokémon first discovered in the Alola region to the Pokédex.",
                null=True,
                validators=[django.core.validators.MaxValueValidator(88)],
                verbose_name="Alola",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_pokedex_entries_gen8",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="This is the Unknown generation at the end of your Pokédex with Meltan and Melmetal.",
                null=True,
                validators=[django.core.validators.MaxValueValidator(2)],
                verbose_name="Galar (Meltan)",
            ),
        ),
        migrations.AddField(
            model_name="update",
            name="badge_pokemon_purified",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Purify 500 Shadow Pokémon.",
                null=True,
                verbose_name="Purifier",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_pokedex_entries_gen3",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Register 90 Pokémon first discovered in the Hoenn region to the Pokédex.",
                null=True,
                validators=[django.core.validators.MaxValueValidator(134)],
                verbose_name="Hoenn",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_pokedex_entries_gen4",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Register 80 Pokémon first discovered in the Sinnoh region to the Pokédex.",
                null=True,
                validators=[django.core.validators.MaxValueValidator(107)],
                verbose_name="Sinnoh",
            ),
        ),
    ]
