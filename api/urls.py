from django.urls import path, include
from rest_framework import routers

from api.player.player import PlayerViewSet

router = routers.DefaultRouter()
router.register('player', PlayerViewSet)

urlpatterns = [
    path('', include(router.urls))
]
