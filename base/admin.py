from django.contrib import admin

from base.models import Log, Player, PlayerSecured, PlayerTemporary, Round, Session

# Register your models here.

admin.site.register(Log)
admin.site.register(Player)
admin.site.register(PlayerSecured)
admin.site.register(PlayerTemporary)
admin.site.register(Round)
admin.site.register(Session)
