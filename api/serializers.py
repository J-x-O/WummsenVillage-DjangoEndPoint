from rest_framework import serializers

from base.models import Player, Session, UserAccount


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            'player_name',
            'player_tag',
            'player_elo'
        ]


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = [
            'player__name',
            'player__tag',
            'elo'
        ]


class SessionSerializer(serializers.ModelSerializer):
    winner = PlayerSerializer(read_only=True)
    players = PlayerSerializer(read_only=True, many=True)

    class Meta:
        model = Session
        fields = [
            'session_id',
            'patch_id',
            'finalized',
            'winner',
            'players'
        ]


class RoundSerializer(serializers.ModelSerializer):
    winner = PlayerSerializer(read_only=True)

    class Meta:
        model = Player
        fields = [
            'round_id',
            'winner',
            'outcome'
        ]


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            'target',
            'start_time',
            'end_time',
            'payload'
        ]
