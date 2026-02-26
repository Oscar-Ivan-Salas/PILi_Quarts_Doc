# Dockerfile for N04 Binary Factory - SOBERANO V10
# Base: Python 3.10 with Playwright support
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos primero para cachear capas
COPY requirements_N04.txt .
RUN pip install --no-cache-dir -r requirements_N04.txt

# Instalar navegadores de Playwright necesarios (Chromium)
RUN playwright install chromium

# Copiar el resto del código
COPY . .

# Variables de entorno por defecto
ENV PORT=8005
ENV HOST=0.0.0.0

# Exponer puerto
EXPOSE 8005

# Comando de arranque
CMD ["python", "studio_api.py"]
