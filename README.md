
# Nova 

[![postgreSQL version](https://img.shields.io/badge/Django-v2.0_v3.0-purple.svg?style=flat-square)](https://www.postgresql.org/)

## Proyecto Desarrollo II 

Para la primera instalación:

```
docker-compose build
docker-compose up
```

y como es la primera vez hay que migrar la prueba de modelo

```
docker exec -it nombre_del_docker_django python manage.py makemigrations
docker exec -it nombre_del_docker_django python manage.py migrate
```

nota: ultima columna es el nombre del docker (debe ser algo como con web)

```
docker ps -a
```