#!bin/sh

echo "Hello"
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata inventario_nova.json
python manage.py loaddata usuarios_nova.json
#echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('nova', '', 'nova')" | python manage.py shell

exec "$@"