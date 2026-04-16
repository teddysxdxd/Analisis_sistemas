FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

# Crear carpeta para la base de datos y dar permisos
RUN mkdir -p /app/data && chmod 777 /app/data

# Exponer puerto e iniciar con Gunicorn (más robusto que el server de Flask)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]