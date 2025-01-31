# Generated by Django 2.1.4 on 2019-02-10 21:03

from django.db import migrations, models
import django.db.models.deletion
import pokemongo.models


def move_sponerships_to_badges(apps, schema_editor):
    Sponsorship = apps.get_model("pokemongo", "Sponsorship")
    ProfileBadge = apps.get_model("pokemongo", "ProfileBadge")
    for x in Sponsorship.objects.all():
        ProfileBadge.objects.create(
            slug=x.slug,
            title=x.title,
            description=x.description,
            badge=x.icon,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("pokemongo", "0022_auto_20190210_2013"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProfileBadge",
            fields=[
                ("slug", models.SlugField(primary_key=True, serialize=False)),
                ("title", models.CharField(db_index=True, max_length=20)),
                ("description", models.CharField(db_index=True, max_length=240)),
                (
                    "badge",
                    models.ImageField(upload_to=pokemongo.models.get_path_for_badges),
                ),
            ],
            options={
                "verbose_name": "Badge",
                "verbose_name_plural": "Badges",
            },
        ),
        migrations.CreateModel(
            name="ProfileBadgeHoldership",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("awarded_on", models.DateTimeField(auto_now_add=True)),
                ("reason_given", models.CharField(max_length=64)),
            ],
        ),
        migrations.RunPython(
            move_sponerships_to_badges, reverse_code=migrations.RunPython.noop
        ),
        migrations.AddField(
            model_name="profilebadgeholdership",
            name="awarded_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="badges_awarded",
                to="pokemongo.Trainer",
            ),
        ),
        migrations.AddField(
            model_name="profilebadgeholdership",
            name="badge",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="pokemongo.ProfileBadge"
            ),
        ),
        migrations.AddField(
            model_name="profilebadgeholdership",
            name="trainer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="pokemongo.Trainer"
            ),
        ),
        migrations.AddField(
            model_name="profilebadge",
            name="members",
            field=models.ManyToManyField(
                through="pokemongo.ProfileBadgeHoldership", to="pokemongo.Trainer"
            ),
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_apac_partner_july_2018_japan",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_apac_partner_july_2018_south_korea",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_chicago_fest_july_2017",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_chicago_fest_july_2018",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_pikachu_outbreak_yokohama_2017",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_safari_zone_europe_2017_09_16",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_safari_zone_europe_2017_10_07",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_safari_zone_europe_2017_10_14",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_top_banana",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_yokosuka_1_sep_2018_kurihama",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_yokosuka_1_sep_2018_mikasa",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_yokosuka_1_sep_2018_verny",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_yokosuka_29_aug_2018_kurihama",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_yokosuka_29_aug_2018_mikasa",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_yokosuka_29_aug_2018_verny",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_yokosuka_2_sep_2018_kurihama",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_yokosuka_2_sep_2018_mikasa",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_yokosuka_2_sep_2018_verny",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_yokosuka_30_aug_2018_kurihama",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_yokosuka_30_aug_2018_mikasa",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_yokosuka_30_aug_2018_verny",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_yokosuka_31_aug_2018_kurihama",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_yokosuka_31_aug_2018_mikasa",
        ),
        migrations.RemoveField(
            model_name="trainer",
            name="badge_yokosuka_31_aug_2018_verny",
        ),
    ]
