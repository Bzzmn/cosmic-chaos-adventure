# Cosmic Chaos Adventure - Backend API

Backend API para el juego Cosmic Chaos Adventure, desarrollado con FastAPI y PostgreSQL.

## Estructura del Proyecto

```
app/
├── api/                  # Definición de endpoints de la API
│   ├── dependencies/     # Dependencias para los endpoints
│   ├── endpoints/        # Endpoints organizados por recursos
│   ├── middlewares/      # Middlewares personalizados
│   └── router.py         # Router principal
├── core/                 # Configuraciones del núcleo de la aplicación
│   └── config.py         # Configuraciones desde variables de entorno
├── db/                   # Configuración y modelos de la base de datos
│   ├── migrations/       # Migraciones de Alembic
│   ├── models/           # Modelos SQLAlchemy
│   ├── repositories/     # Repositorios para acceso a datos
│   └── session.py        # Configuración de sesión de BD
├── services/             # Lógica de negocio
├── tests/                # Tests para la aplicación
└── utils/                # Utilidades y funciones auxiliares
```

## Requisitos

- Python 3.10+
- PostgreSQL 14+

## Configuración del Entorno de Desarrollo

1. Clonar el repositorio:
   ```
   git clone https://github.com/tuusuario/cosmic-chaos-adventure.git
   cd cosmic-chaos-adventure/back-fastapi
   ```

2. Crear un entorno virtual y activarlo:
   ```
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Crear un archivo `.env` basado en `.env.example` con tus configuraciones.

5. Crear la base de datos en PostgreSQL:
   ```
   createdb cosmic_chaos_dev
   ```

6. Aplicar las migraciones:
   ```
   alembic upgrade head
   ```

7. Ejecutar la aplicación en modo desarrollo:
   ```
   uvicorn main:app --reload
   ```

8. Acceder a la documentación de la API:
   ```
   http://localhost:8000/docs
   ```

## Comandos Útiles

- **Ejecutar tests**:
  ```
  pytest
  ```

- **Formatear código**:
  ```
  black app/
  ```

- **Ejecutar linter**:
  ```
  flake8 app/
  ```

- **Ordenar imports**:
  ```
  isort app/
  ``` 