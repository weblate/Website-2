# Generated by Django 2.1.7 on 2019-02-23 21:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pokemongo", "0025_merge_20190216_1542"),
    ]

    operations = [
        migrations.AddField(
            model_name="update",
            name="badge_photobomb",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Have 𝓍 surprise encounters in AR Snapshot.",
                null=True,
                verbose_name="Cameraman",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_pokedex_entries_gen2",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Register 70 Pokémon first discovered in the Johto region to the Pokédex.",
                null=True,
                validators=[django.core.validators.MaxValueValidator(100)],
                verbose_name="Johto",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_pokedex_entries_gen3",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Register 90 Pokémon first discovered in the Hoenn region to the Pokédex.",
                null=True,
                validators=[django.core.validators.MaxValueValidator(133)],
                verbose_name="Hoenn",
            ),
        ),
    ]
