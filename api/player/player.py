import django_filters
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth import IsReadOnly, IsReadOnlyOrAdmin
from api.utility import validate_required_params, validate_required_param, validate_json_params
from api.serializers import PlayerSerializer, PlayerPostSerializer
from base.models import Player, Session


class PlayerNotFoundException(APIException):
    status_code = 400
    default_detail = 'Player does not exist'
    default_code = 'bad_request'


class PlayerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    # filterset_fields = ('player_name', 'player_tag')

    @action(detail=False, methods=['GET'], url_path='get_player')
    def get_player(self, request: Request, *args, **kwargs):
        """
            Fetches the Player using the provided data
            Required: Definition of player with { "player_name": string, "player_tag": int }
        """
        required_params = ['player_name', 'player_tag']
        player_name, player_tag = validate_required_params(request, required_params)
        try:
            player = Player.objects.get(player_name=player_name, player_tag=player_tag)
            serializer = PlayerSerializer(player)
            return Response(serializer.data)
        except Player.DoesNotExist:
            raise PlayerNotFoundException()



class GetPlayers(APIView):
    """
        Fetches a list of Players using the provided data
        Required: List of players with { "player_name": string, "player_tag": int }
    """
    parser_classes = [JSONParser]

    def get(self, request, format=None):
        player_definitions = validate_required_param(request, 'players')
        players = []
        for player_data in player_definitions:
            name, tag = validate_json_params(player_data, ['name', 'tag'])
            try:
                player: Player = Player.objects.get(player_name=name, player_tag=tag)
                players.append(player)
            except Player.DoesNotExist:
                pass

        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)
