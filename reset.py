import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoEndPoint.settings")
django.setup()

os.system('python manage.py reset_db')
os.system('python manage.py makemigrations')
os.system('python manage.py migrate')

from django.contrib.auth.models import User
User.objects.create_superuser('Jesco', 'JescoVogt@web.de', 'Brut4lR3inWumms3n')
