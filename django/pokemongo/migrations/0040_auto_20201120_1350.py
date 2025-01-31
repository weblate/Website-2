# Generated by Django 2.2.17 on 2020-11-20 13:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pokemongo", "0039_auto_20200912_0000"),
    ]

    operations = [
        migrations.AddField(
            model_name="trainer",
            name="legacy_40",
            field=models.BooleanField(
                default=False,
                help_text="Achieve level 40 by December 31, 2020.",
                verbose_name="Legacy 40",
            ),
        ),
        migrations.AddField(
            model_name="update",
            name="badge_7_day_streaks",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Achieve a Pokémon catch streak or PokéStop spin streak of seven days 100 times.",
                null=True,
                verbose_name="Triathlete",
            ),
        ),
        migrations.AddField(
            model_name="update",
            name="badge_pokemon_caught_at_your_lures",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Catch 2500 Pokémon attracted by a Lure Module.",
                null=True,
                verbose_name="Mega Evolution Guru",
            ),
        ),
        migrations.AddField(
            model_name="update",
            name="badge_unique_pokestops",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Visit 2000 unique PokéStops.",
                null=True,
                verbose_name="Sightseer",
            ),
        ),
        migrations.AddField(
            model_name="update",
            name="badge_unique_raid_bosses_defeated",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Defeat 150 different species of Pokémon in raids.",
                null=True,
                verbose_name="Rising Star",
            ),
        ),
        migrations.AlterField(
            model_name="community",
            name="language",
            field=models.CharField(
                choices=[
                    ("de-DE", "German"),
                    ("en-US", "English"),
                    ("es-ES", "Spanish"),
                    ("fr-FR", "French"),
                    ("it-IT", "Italian"),
                    ("ja-JP", "Japanese"),
                    ("ko-KR", "Korean"),
                    ("nl-NL", "Dutch"),
                    ("nl-BE", "Dutch, Belgium"),
                    ("ro-RO", "Romanian"),
                    ("ru-RU", "Russian"),
                    ("pt-BR", "Brazilian Portuguese"),
                    ("th-TH", "Thai"),
                    ("zh-HK", "Traditional Chinese"),
                ],
                default="en-US",
                max_length=5,
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_battle_attack_won",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Win 4000 Gym battles.",
                null=True,
                verbose_name="Battle Girl",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_battle_training_won",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Train 2000 times.",
                null=True,
                verbose_name="Ace Trainer",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_berries_fed",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Feed 15000 Berries at Gyms.",
                null=True,
                verbose_name="Berry Master",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_big_magikarp",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Catch 1000 big Magikarp.",
                null=True,
                verbose_name="Fisher",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_buddy_best",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Have 200 Best Buddies.",
                null=True,
                verbose_name="Best Buddy",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_capture_total",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Catch 50000 Pokémon.",
                null=True,
                verbose_name="Collector",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_challenge_quests",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Complete 2500 Field Research tasks.",
                null=True,
                verbose_name="Pokémon Ranger",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_evolved_total",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Evolve 2000 Pokémon.",
                null=True,
                verbose_name="Scientist",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_great_league",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Win 1000 Trainer Battles in the Great League.",
                null=True,
                verbose_name="Great League Veteran",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_hatched_total",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Hatch 2500 eggs.",
                null=True,
                verbose_name="Breeder",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_hours_defended",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Defend Gyms for 15000 hours.",
                null=True,
                verbose_name="Gym Leader",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_legendary_battle_won",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Win 2000 Legendary raids.",
                null=True,
                verbose_name="Battle Legend",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_master_league",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Win 1000 Trainer Battles in the Master League.",
                null=True,
                verbose_name="Master League Veteran",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_max_level_friends",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Become Best Friends with 20 Trainers.",
                null=True,
                verbose_name="Idol",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_photobomb",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Have 400 surprise encounters in GO Snapshot.",
                null=True,
                verbose_name="Cameraman",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_pikachu",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Catch 1000 Pikachu.",
                null=True,
                verbose_name="Pikachu Fan",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_pokedex_entries",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Register 151 Kanto region Pokémon in the Pokédex.",
                null=True,
                validators=[django.core.validators.MaxValueValidator(151)],
                verbose_name="Kanto",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_pokedex_entries_gen2",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Register 100 Pokémon first discovered in the Johto region to the Pokédex.",
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
                help_text="Register 135 Pokémon first discovered in the Hoenn region to the Pokédex.",
                null=True,
                validators=[django.core.validators.MaxValueValidator(135)],
                verbose_name="Hoenn",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_pokedex_entries_gen4",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Register 107 Pokémon first discovered in the Sinnoh region to the Pokédex.",
                null=True,
                validators=[django.core.validators.MaxValueValidator(107)],
                verbose_name="Sinnoh",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_pokemon_purified",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Purify 1000 Shadow Pokémon.",
                null=True,
                verbose_name="Purifier",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_pokestops_visited",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Visit 50000 PokéStops.",
                null=True,
                verbose_name="Backpacker",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_raid_battle_won",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Win 2000 raids.",
                null=True,
                verbose_name="Champion",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_rocket_giovanni_defeated",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Defeat the Team GO Rocket Boss 50 times. ",
                null=True,
                verbose_name="Ultra Hero",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_rocket_grunts_defeated",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Defeat 2000 Team GO Rocket Grunts.",
                null=True,
                verbose_name="Hero",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_small_rattata",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Catch 1000 tiny Rattata.",
                null=True,
                verbose_name="Youngster",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_total_mega_evos",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Mega Evolve a Pokémon 1000 times.",
                null=True,
                verbose_name="Successor",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_trading",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Trade 2500 Pokémon.",
                null=True,
                verbose_name="Gentleman",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_trading_distance",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Earn 10000000 km across the distance of all Pokémon trades.",
                null=True,
                verbose_name="Pilot",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_travel_km",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                help_text="Walk 10,000 km.",
                max_digits=16,
                null=True,
                verbose_name="Jogger",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_ultra_league",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Win 1000 Trainer Battles in the Ultra League.",
                null=True,
                verbose_name="Ultra League Veteran",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_unique_mega_evos",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Mega Evolve 46 different species of Pokémon.",
                null=True,
                verbose_name="Mega Evolution Guru",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_unown",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Catch 28 Unown.",
                null=True,
                validators=[django.core.validators.MaxValueValidator(28)],
                verbose_name="Unown",
            ),
        ),
        migrations.AlterField(
            model_name="update",
            name="badge_wayfarer",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Earn 1500 Wayfarer Agreements",
                null=True,
                verbose_name="Wayfarer",
            ),
        ),
    ]
