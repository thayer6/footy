from django.db import models
from django.utils import timezone

# epl stats
# epl schedule
class Table(models.Model):
    rank = models.IntegerField(null = True)
    squad = models.CharField(null = True, blank=True, max_length=255)
    games = models.IntegerField(null=True)
    wins = models.IntegerField(null=True)
    draws = models.IntegerField(null=True)
    losses = models.IntegerField(null=True)
    goals_for = models.IntegerField(null=True)
    goals_against = models.IntegerField(null=True)
    goals_difference = models.IntegerField(null=True)
    points = models.IntegerField(null=True)

    class Admin:
        pass
