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

# class ResultsFixtures(models.Model):
#     week = models.IntegerField(null=True)
#     day = models.CharField(null=True, blank = True, max_length=250)
#     date = models.DateField(null = True, blank=True)
#     time = models.TimeField(null=True, blank=True)
#     home = models.CharField(null=True, blank=True, max_length=250)
#     xg_h = models.DoubleField(null=True, blank = True)
#     score = models.CharField(null=True, blank=True, max_length=250)
#     xg_a = models.DoubleField(null=True, blank = True)
#     away = models.CharField(null=True, blank=True)
#     attendance = models.IntegerField(null=True)
#     venue = models.CharField(null=True, blank = True)
#     referee = models.CharField(null=True, blank=True)

#     class Admin:
#         pass

#class Stats(models.Model):
    # squad = models.CharField(null=True, blank=True, max_length=250)
    # players_used = models.IntegerField(null=True)
    # avg_age = models.DoubleField(null=True)
    # possession = models.DoubleField(null=True)
    # games = models.IntegerField(null=True)
    # game_starts = models.IntegerField(null=True)
    # minutes = models.IntegerField(null=True)
    # minutes_90 = models.DoubleField(null=True)
    # goals = models.IntegerField(null=True)
    # assists = models.IntegerField(null=True)
    # goals_pens = models.IntegerField(null=True)
    # pens_made = models.IntegerField(null=True)
    # pens_att = models.IntegerField(null=True)
    # cards_yellow = models.IntegerField(null=True)
    # cards_red = models.IntegerField(null=True)
    # goals_per90 = models.DoubleField(null=True)
    # assists_per90 = models.DoubleField(null=True)
    # goals_assists_per90 = models.DoubleField(null=True)
    # goals_pens_per90 = models.DoubleField(null=True)
    # goals_assists_pens_per90 = models.DoubleField(null=True)
    # xg = models.DoubleField(null=True)
    # npxg = models.DoubleField(null=True)
    # xa = models.DoubleField(null=True)
    # xa_per90 = models.DoubleField(null=True)
    # xg_xa_per90 = models.DoubleField(null=True)
    # npxg_per90 = models.DoubleField(null=True)
    # npxg_xa_per90 = models.DoubleField(null=True)
    # 
    # class Admin:
#       pass