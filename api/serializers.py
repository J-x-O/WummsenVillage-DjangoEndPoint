from rest_framework import serializers

from base.models import Player, Session, UserAccount


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            'name',
            'tag',
        ]


class UserAccountSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()

    def get_name(self, obj): return obj.player.name
    def get_tag(self, obj): return obj.player.name

    class Meta:
        model = UserAccount
        fields = [
            'name',
            'tag',
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
