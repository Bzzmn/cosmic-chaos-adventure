# Migraciones de Base de Datos

Esta carpeta contiene las migraciones de la base de datos gestionadas por Alembic.

## Estructura

- `versions/`: Contiene las versiones de migraciones
- `env.py`: Entorno de configuración para Alembic
- `script.py.mako`: Plantilla para generar archivos de migración
- `alembic.ini`: Archivo de configuración de Alembic

## Comandos útiles

Para inicializar Alembic (primera vez):
```
alembic init migrations
```

Para crear una nueva migración:
```
alembic revision --autogenerate -m "descripción del cambio"
```

Para aplicar todas las migraciones pendientes:
```
alembic upgrade head
```

Para revertir la última migración:
```
alembic downgrade -1
``` 