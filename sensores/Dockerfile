# Usamos una versión ligera de Python
FROM python:3.9-slim

# Establecemos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Instalamos las librerías necesarias UNA SOLA VEZ
RUN pip install pika

# Copiamos el código (opcional si usas volúmenes, pero buena práctica)
COPY . .

# Comando por defecto al iniciar (el -u es para ver logs en tiempo real)
CMD ["python", "-u", "productor_sensor.py"]
