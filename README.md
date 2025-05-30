# Tus datos backend 👥

## 1. Resumen 📘

Tus datos es un proyecto de código abierto que proporciona una plataforma para la gestión y organizacion de eventos.

Publico objetivo:

-   👩‍💻 Emprendedores
-   🚀 Comunidades
-   🏢 Empresa

## 3. Funcionalidades ✨

-   **Registro de usuario**: Permite a los usuarios registrarse y crear un perfil.
-   **Creación de eventos**: Los usuarios pueden crear y gestionar eventos, incluyendo la carga de imágenes y la configuración de detalles del evento.
-   **Exploración de eventos**: Los usuarios pueden explorar eventos creados por otros, con opciones de filtrado y búsqueda.

## 4. Tech Stack 🛠️

**Backend:** Python, FastAPI
**ORM:** SQLAlchemy
**Base de datos:** PostgreSQL
**Migraciones:** Alembic



## 5. Resumen de la estructura del proyecto 📂

La aplicación está construida con FastAPI y Python. 

a continuación una pequeña descripción de la estructura del proyecto:

```
src/app/
├── core/                # configuración y utilidades de la aplicación
├── db/                  # Base de datos y modelos
├── modules/             # Codigo modularizado por funcionalidades y rutas
├── shared/              # Codigo compartido entre modulos
└── main.py              # Punto de entrada de la aplicación
```

## 6. Setup e instalación ⚙️

```bash
# 1. crear un entorno virtual
python -m venv venv

# 2. activar el entorno virtual
# En Windows
venv\Scripts\activate

# En Linux o MacOS
source venv/bin/activate

# Clonar repositorio
git clone https://github.com/pizza-and-juice/eventosb
cd eventosb

# Instalar Poetry
pip install poetry

# Instalar dependencias
poetry install

# Comenzar la app
poetry run uvicorn src.app.main:app --reload
```

### 7 .env 🔐

Create a `.env` file in the root directory of the project, using .env.example as a template.

| Variable Name    | Description                                           |
|------------------|-------------------------------------------------------|
| `DB_NAME`        | Nombre de la base de datos PostgreSQL                 |
| `DB_USER`        | Usuario de la base de datos PostgreSQL                |
| `DB_PASSWORD`    | Contraseña del usuario de la base de datos PostgreSQL |
| `DB_HOST`        | Host de la base de datos PostgreSQL                   |
| `DB_PORT`        | Puerto de la base de datos Postgre                    |
| `JWT_SECRET_KEY` | Clave secreta para la firma de tokens JWT             |


## 8. Ramas Git 🌿

1. main -> producción
