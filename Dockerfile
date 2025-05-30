# Etapa base
FROM python:3.12.4

# Instala Poetry
RUN pip install poetry

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de configuración primero
COPY pyproject.toml poetry.lock* /app/

# Instala dependencias
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

# Copia el resto del código
COPY . .

# Exponer puerto de FastAPI
EXPOSE 8000

# Comando de arranque
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
