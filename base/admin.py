from django.contrib import admin

from base.models import Log, Player, PlayerSecured, UserTemporary, Round, Session

# Register your models here.

admin.site.register(Log)
admin.site.register(Player)
admin.site.register(PlayerSecured)
admin.site.register(UserTemporary)
admin.site.register(Round)
admin.site.register(Session)
