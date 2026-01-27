FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.6.1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    tesseract-ocr \
    tesseract-ocr-spa \
    tesseract-ocr-eng \
    poppler-utils \
    libmagic1 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY pyproject.toml poetry.lock* ./

# Instalar dependencias de Python
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copiar el resto de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p /app/storage/documents \
    && mkdir -p /app/storage/generated \
    && mkdir -p /app/storage/vector_store

# Instalar la aplicación en modo desarrollo
RUN pip install -e .

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]