import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoEndPoint.settings")
django.setup()

os.system('python manage.py reset_db')
os.system('python manage.py makemigrations')
os.system('python manage.py migrate')

from base.models import User, UserAccount, Player

# create working account
user: User = User.objects.create_superuser('JescoVogt@web.de', 'Brut4lR3inWumms3n')
account: UserAccount = UserAccount.objects.create(user=user)
player: Player = Player.objects.create(user=account, name="Jesco", tag=1111)
account.player = player
account.save()

User.objects.create_web_user('WebAccess@WebAccess.de', 'W3bAcc3ss')
