FROM python:3.9-slim

WORKDIR /app

# Aquí instalamos requests también
RUN pip install pika requests websockets

COPY . .

CMD ["python", "-u", "procesador_alertas.py"]
