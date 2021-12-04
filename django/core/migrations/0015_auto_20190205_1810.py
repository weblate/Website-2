# Generated by Django 2.1.4 on 2019-02-05 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("socialaccount", "0003_extra_data_default_dict"),
        ("core", "0014_discordguildmembership_nick_override"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiscordUser",
            fields=[],
            options={
                "verbose_name": "Discord User",
                "verbose_name_plural": "Discord Users",
                "proxy": True,
                "indexes": [],
            },
            bases=("socialaccount.socialaccount",),
        ),
        migrations.AlterField(
            model_name="discordguild",
            name="members",
            field=models.ManyToManyField(
                through="core.DiscordGuildMembership", to="core.DiscordUser"
            ),
        ),
        migrations.AlterField(
            model_name="discordguildmembership",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.DiscordUser"
            ),
        ),
    ]
