# Generated by Django 2.1.3 on 2018-12-08 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pokemongo", "0014_auto_20181208_1439"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="nickname",
            options={"ordering": ["nickname"]},
        ),
    ]
