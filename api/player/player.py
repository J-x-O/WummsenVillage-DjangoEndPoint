import django_filters
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth import IsReadOnly, IsReadOnlyOrAdmin
from api.utility import validate_required_params, validate_required_param, validate_json_params, extract_json, \
    extract_optional_param
from api.serializers import PlayerSerializer, PlayerPostSerializer
from base.models import Player, Session, UserAccount


class PlayerNotFoundException(APIException):
    status_code = 400
    default_detail = 'Player does not exist'
    default_code = 'bad_request'


class PlayerCantBeAccessedException(APIException):
    status_code = 400
    default_detail = 'Please provide a valid AccessToken'
    default_code = 'bad_request'

def check_access(self, user: User, target: UserAccount):
    if user.is_secured and\
            not request.user.is_admin and\
            not request.user.is_moderator and\
            not player.player_secured.can_be_accessed(request.user, access_token=access_token):
        raise PlayerCantBeAccessedException


class PlayerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], url_path='get_one')
    def get_player(self, request: Request):
        """
            Fetches the Player using the provided data
            Required: Definition of player with { "player_name": string, "player_tag": int }
        """
        json = extract_json(request)
        name, tag = validate_json_params(json, ['name', 'tag'])
        access_token = json.get('access_token', None)

        try:
            player = UserAccount.objects.get(player__name=name, player__tag=tag)
            serializer = PlayerSerializer(player)
        except Player.DoesNotExist:
            raise PlayerNotFoundException()

        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='get_many')
    def get_players(self, request: Request):
        """
            Fetches multiple Players using the provided data
            Required: List of players defined like { "name": string, "tag": int }
        """
        player_definitions = validate_required_param(request, 'players')
        players = []
        for player_data in player_definitions:
            name, tag = validate_json_params(player_data, ['name', 'tag'])
            try:
                player: Player = Player.objects.get(name=name, tag=tag)
                players.append(player)
            except Player.DoesNotExist:
                pass

        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)



