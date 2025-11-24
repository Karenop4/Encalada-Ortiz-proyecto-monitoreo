import pika
import json
import asyncio
import websockets

# URL del servidor WebSocket (Debe coincidir con el nombre del servicio en docker-compose)
WS_URL = "ws://websocket:9000"

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='alertas_cuenca')

print("Procesador activo. Esperando mensajes...")

# --- Función para enviar la alerta al servidor WebSocket ---
async def enviar_ws(alerta):
    try:
        async with websockets.connect(WS_URL) as ws:
            await ws.send(json.dumps(alerta))
            print(f"📡 Enviado al WS: {alerta['alerta']}")
    except Exception as e:
        print(f" Error conectando al WS: {e}")

# --- Callback que se ejecuta por cada mensaje de RabbitMQ ---
def callback(ch, method, properties, body):
    mensaje = json.loads(body)

    sensor = mensaje["sensor_id"]
    tipo = mensaje["tipo"]
    valor = mensaje["valor"]

    # --- Clasificación de alerta ---
    alerta_procesada = {
        "alerta": "Evento Normal",
        "nivel": "verde",
        "mensaje": f"Sensor {sensor} operando normalmente",
        "sensor_id": sensor,
        "timestamp": mensaje["timestamp"]
    }

    # LÓGICA DE NEGOCIO
    if tipo == "temperatura":
        if valor > 45:
            alerta_procesada.update({"alerta": " CALOR CRÍTICO", "nivel": "rojo", "mensaje": f"¡Peligro! {valor}°C"})
        elif valor > 35:
            alerta_procesada.update({"alerta": " Advertencia Calor", "nivel": "amarillo", "mensaje": f"Temp: {valor}°C"})
    elif tipo == "humo" and valor == 1:
        alerta_procesada.update({"alerta": " INCENDIO", "nivel": "rojo", "mensaje": "Humo detectado"})
    elif tipo == "puerta" and valor == "abierta":
        alerta_procesada.update({"alerta": " Puerta Abierta", "nivel": "amarillo", "mensaje": "Acceso no autorizado"})
    elif tipo == "movimiento" and valor == "detectado":
        alerta_procesada.update({"alerta": " Movimiento", "nivel": "amarillo", "mensaje": "Movimiento detectado"})

    # --- Enviar la alerta al WebSocket ---
    try:
        asyncio.run(enviar_ws(alerta_procesada))
    except Exception as e:
        print(f"Error en loop asíncrono: {e}")

# --- Consumir mensajes de RabbitMQ ---
channel.basic_consume(queue='alertas_cuenca', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
