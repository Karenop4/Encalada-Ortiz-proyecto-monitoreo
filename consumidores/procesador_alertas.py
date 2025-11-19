import pika
import json
import asyncio
import websockets

# URL del servidor WebSocket
WS_URL = "ws://localhost:9000"

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='alertas_cuenca')

print("Procesador activo. Esperando mensajes...")

# --- Función para enviar la alerta al servidor WebSocket ---
async def enviar_ws(alerta):
    try:
        async with websockets.connect(WS_URL) as ws:
            await ws.send(json.dumps(alerta))
    except Exception as e:
        print("❌ No se pudo enviar al WebSocket:", e)
        print("Dato procesado localmente:", alerta)

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

    if tipo == "temperatura":
        if valor > 45:
            alerta_procesada.update({
                "alerta": "🔥 CALOR CRÍTICO",
                "nivel": "rojo",
                "mensaje": f"¡Peligro! {valor}°C en {sensor}"
            })
        elif valor > 35:
            alerta_procesada.update({
                "alerta": "⚠️ Advertencia Calor",
                "nivel": "amarillo",
                "mensaje": f"Subiendo temperatura: {valor}°C"
            })
    elif tipo == "humo" and valor == 1:
        alerta_procesada.update({
            "alerta": "🚨 INCENDIO DETECTADO",
            "nivel": "rojo",
            "mensaje": f"Humo detectado en sensor {sensor}"
        })
    elif tipo == "puerta" and valor == "abierta":
        alerta_procesada.update({
            "alerta": "🚪 Puerta Abierta",
            "nivel": "amarillo",
            "mensaje": f"Acceso en {sensor}"
        })
    elif tipo == "movimiento" and valor == "detectado":
        alerta_procesada.update({
            "alerta": "👀 Movimiento Detectado",
            "nivel": "amarillo",
            "mensaje": f"Movimiento en {sensor}"
        })

    # --- Enviar la alerta al WebSocket ---
    asyncio.run(enviar_ws(alerta_procesada))

    print(f"✅ Procesado y enviado: {alerta_procesada['alerta']}")

# --- Consumir mensajes de RabbitMQ ---
channel.basic_consume(queue='alertas_cuenca', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
