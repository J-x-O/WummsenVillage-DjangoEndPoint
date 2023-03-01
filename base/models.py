import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, name: str, tag: int, email: str, password=None):
        """ Creates and saves a User with the given email. """
        email = self.normalize_email(email)
        if not email:
            raise ValueError('Users must have a valid email address')

        player = Player.objects.get_or_create(name=name, tag=tag)
        user = self.model(
            player=player,
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name: str, tag: int, email: str, password=None):
        """ Creates and saves a superuser with the given email and password. """
        user = self.create_user(name, tag, email, password=password)
        user.is_admin = True
        user.is_moderator = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.CharField(max_length=100)
    is_admin = models.BooleanField(blank=True, default=False)
    is_moderator = models.BooleanField(blank=True, default=False)

    USERNAME_FIELD = 'email'


class UserAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    player = models.OneToOneField('Player', on_delete=models.DO_NOTHING)
    elo = models.IntegerField(default=1000, blank=True)
    gatekeep_access = models.BooleanField(blank=True, default=False)
    access_password = models.CharField(max_length=128, blank=True, null=True, default=None)

    def can_be_accessed(self, accessing_user, access_token=None):
        if not self.gatekeep_access:
            return True
        try:
            access = AccessGranted.objects.get(player_from=self, player_to=accessing_user)
            return access.access_token is None or access.access_token == access_token
        except AccessGranted.DoesNotExist:
            return False


class PlayerManager(models.Manager):
    def get_or_create(self, *args, **kwargs):
        try:
            return self.get(args, kwargs)
        except self.model.DoesNotExist:
            return self.create(kwargs)


class Player(models.Model):
    class Meta:
        unique_together = ('player_name', 'player_tag')

    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    tag = models.PositiveSmallIntegerField()
    objects = PlayerManager()

    @property
    def is_secured(self):
        return hasattr(self, 'player_secured')


class AccessGranted(models.Model):
    class Meta:
        unique_together = ('player_from', 'player_to')

    user_from = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    user_to = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=10, blank=True, null=True, default=None)


class UserTemporary(models.Model):
    """ Used for Email Verification """
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, primary_key=True)
    temporary_password = models.CharField(max_length=32)


# ----------------------------------------------------------------------------------------------------------------------


class Session(models.Model):
    session_id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    patch_id = models.CharField(max_length=10)
    session_owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
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
