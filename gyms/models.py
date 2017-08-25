#from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.gis.db import models

class Town(models.Model):
    name = models.CharField(max_length=64)
    poly = models.PolygonField()
    discord_webhook = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Gym(models.Model):
    TEAM_UNCONTESTED = 0
    TEAM_MYSTIC = 1
    TEAM_VALOR = 2
    TEAM_INSTINCT = 3

    TEAM_CHOICES = (
        (TEAM_UNCONTESTED, 'Uncontested'),
        (TEAM_MYSTIC, 'Mystic'),
        (TEAM_INSTINCT, 'Instinct'),
    )

    enabled = models.BooleanField()
    guard_pokemon_id = models.IntegerField()
    id = models.CharField(max_length=64, primary_key=True)
    last_modified = models.DateTimeField()
    last_scanned = models.DateTimeField(null=True, blank=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    name = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    
    team = models.IntegerField(choices=TEAM_CHOICES)
    slots_available = models.IntegerField()
    raid_start = models.DateTimeField(null=True, blank=True)
    raid_end = models.DateTimeField(null=True, blank=True)
    raid_level = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)],
                                     null=True, blank=True)
    raid_pokemon_id = models.PositiveIntegerField(null=True, blank=True)
    raid_pokemon_name = models.CharField(max_length=64, null=True, blank=True)
    raid_pokemon_cp = models.PositiveIntegerField(null=True, blank=True)
    raid_pokemon_move_1 = models.PositiveIntegerField(null=True, blank=True)
    raid_pokemon_move_2 = models.PositiveIntegerField(null=True, blank=True)
    notification_sent_at = models.DateTimeField()
    town = models.ForeignKey(Town, null=True, blank=True)

    def is_raid_active(self):
        if self.raid_start and self.raid_end and timezone.now() >= self.raid_start and timezone.now() <= self.raid_end:
            return True
        return False
