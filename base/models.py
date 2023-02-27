import uuid
from django.db import models


class Player(models.Model):
    class Meta:
        unique_together = ('player_name', 'player_tag')

    player_name = models.CharField(max_length=32)
    player_tag = models.PositiveSmallIntegerField()
    player_elo = models.IntegerField(default=1000, blank=True)


class PlayerSecured(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True)
    player_email = models.CharField(max_length=100)
    player_password = models.CharField(max_length=32)


class PlayerTemporary(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True)
    player_temporary_password = models.CharField(max_length=32)


# ----------------------------------------------------------------------------------------------------------------------


class Session(models.Model):
    session_id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    patch_id = models.CharField(max_length=10)
    finalized = models.BooleanField(default=False, blank=True)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='won_sessions', null=True, blank=True, default=None)
    players = models.ManyToManyField(Player, related_name='played_sessions', blank=True)


class Round(models.Model):
    class Meta:
        unique_together = ('session', 'round_id')

    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    round_id = models.PositiveSmallIntegerField()
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, blank=True, default=None)
    outcome = models.CharField(max_length=10, blank=True, default="")


class Log(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    target = models.CharField(max_length=32)
    start_time = models.TimeField()
    end_time = models.TimeField()
    payload = models.CharField(max_length=150)
