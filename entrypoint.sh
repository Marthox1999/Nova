#!bin/sh

echo "Hello"
python manage.py makemigrations inventario
python manage.py makemigrations usuarios
python manage.py makemigrations ventas
python manage.py migrate

python manage.py loaddata inventario_nova.json
python manage.py loaddata usuarios_nova.json
python manage.py loaddata ventas_nova.json



exec "$@"
