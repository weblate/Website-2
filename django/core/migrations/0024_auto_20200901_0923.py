# Generated by Django 2.2.16 on 2020-09-01 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0023_auto_20200829_1245"),
    ]

    operations = [
        migrations.AlterField(
            model_name="discordguildsettings",
            name="renamer_with_level_format",
            field=models.CharField(
                choices=[("int", "40"), ("circled_level", "㊵")],
                default="int",
                max_length=50,
                verbose_name="Level Indicator format",
            ),
        ),
    ]
