# Generated by Django 2.2.17 on 2020-11-20 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0025_auto_20200912_0000"),
    ]

    operations = [
        migrations.AlterField(
            model_name="discordguildsettings",
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
    ]
