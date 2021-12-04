# Generated by Django 2.1.3 on 2018-12-08 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pokemongo", "0010_auto_20181208_1319"),
    ]

    operations = [
        migrations.AddField(
            model_name="community",
            name="privacy_public_join",
            field=models.BooleanField(
                default=False,
                help_text="By default, this is off. Turn this on to make your community free to join. No invites required.",
                verbose_name="Publicly Joinable",
            ),
        ),
        migrations.AddField(
            model_name="community",
            name="privacy_tournaments",
            field=models.BooleanField(
                default=False,
                help_text="By default, this is off. Turn this on to share your tournament results with the world.",
                verbose_name="Tournament: Publicly Viewable",
            ),
        ),
        migrations.AlterField(
            model_name="community",
            name="privacy_public",
            field=models.BooleanField(
                default=False,
                help_text="By default, this is off. Turn this on to share your community with the world.",
                verbose_name="Publicly Viewable",
            ),
        ),
    ]
