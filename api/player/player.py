from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.auth import IsReadOnly, IsReadOnlyOrAdmin
from api.player.player_definition import PlayerDefinitionSerializer, PlayerDefinition
from api.utility import validate_required_param, validate_json_params, extract_json, MissingParametersException
from api.serializers import PlayerSerializer, UserAccountSerializer
from base.models import Player, UserAccount, User, AccessGranted


class PlayerNotFoundException(APIException):
    status_code = 400
    default_detail = 'User does not exist'
    default_code = 'bad_request'


class PlayerCantBeAccessedException(APIException):
    status_code = 400
    default_detail = 'Please provide a valid AccessToken'
    default_code = 'bad_request'


def extract_player_data(request, definition: PlayerDefinition):

    if definition.local:
        account: UserAccount = request.user.useraccount
        player: Player = account.local_players.get_or_create(name=definition.name, tag=definition.tag)
        serializer = PlayerSerializer(player)
        return serializer.data
    else:
        user = UserAccount.objects.get(player__name=definition.name, player__tag=definition.tag)
        check_access(request.user, user, definition.access_token)
        track_access(request.user, user)
        serializer = UserAccountSerializer(user)
        return serializer.data




def check_access(user: User, target: UserAccount, access_token: str):
    if target.gatekeep_access and\
            not user.is_admin and\
            not user.is_moderator and\
            not target.can_be_accessed(user, access_token=access_token):
        raise PlayerCantBeAccessedException


def track_access(user: User, target: UserAccount):
    if not target.gatekeep_access and not user.is_admin and not user.is_moderator:
        AccessGranted.objects.get_or_create(user_from=target, user_to=user.useraccount)


class PlayerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], url_path='validate_one')
    def validate_player(self, request: Request):
        """
            Fetches the Player using the provided data
            Required: Definition of player with { "player_name": string, "player_tag": int }
        """
        serializer = PlayerDefinitionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            data = extract_player_data(request, serializer.create(serializer.validated_data))
            return Response(data)
        except UserAccount.DoesNotExist:
            raise PlayerNotFoundException()

    @action(detail=False, methods=['GET'], url_path='validate_many')
    def validate_players(self, request: Request):
        """
            Fetches multiple Players using the provided data
            Required: List of players defined like { "name": string, "tag": int }
        """
        serializer = PlayerDefinitionSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        players = []
        for player_data in serializer.create(serializer.validated_data):
            try:
                data = extract_player_data(request, player_data)
                data["success"] = True
                data["local"] = player_data.local
                players.append(data)
            except UserAccount.DoesNotExist:
                players.append({"success": False, "message": "Target User does not exist"})
            except PlayerCantBeAccessedException:
                players.append({"success": False, "message": PlayerCantBeAccessedException.default_detail})

        return Response(players)



