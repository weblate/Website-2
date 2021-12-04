# Generated by Django 2.2.17 on 2020-11-26 12:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pokemongo", "0043_update_help_string_for_badge_pokemon_caught_at_your_lures"),
    ]

    operations = [
        migrations.AddField(
            model_name="update",
            name="badge_pokedex_entries_gen6",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Register 72 Pokémon first discovered in the Kalos region to the Pokédex.",
                null=True,
                validators=[django.core.validators.MaxValueValidator(72)],
                verbose_name="Kalos",
            ),
        ),
    ]
