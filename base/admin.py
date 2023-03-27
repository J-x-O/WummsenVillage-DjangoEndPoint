from django.contrib import admin

from base.models import Log, Player, Round, Session, User, UserAccount, AccessGranted, UserTemporary

# Register your models here.
admin.site.register(User)
admin.site.register(UserAccount)
admin.site.register(Player)
admin.site.register(AccessGranted)
admin.site.register(UserTemporary)

admin.site.register(Round)
admin.site.register(Session)
admin.site.register(Log)
