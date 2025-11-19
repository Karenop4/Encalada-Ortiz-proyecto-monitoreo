import pika
import json
import time
import random
from datetime import datetime

# 1. Configuración de conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='alertas_cuenca') # Creamos la cola

# IDs de sensores simulados
sensores = ["S-101", "S-102", "S-103", "S-104"]
tipos = ["temperatura", "humo", "movimiento", "puerta"]

print("Sensores activos. Enviando datos al Centro de Control...")

try:
    while True:
        # 2. Simulación de datos (Generamos valores aleatorios)
        sensor_id = random.choice(sensores)
        tipo_evento = random.choice(tipos)
        valor = 0

        # Lógica simple para dar valores realistas
        if tipo_evento == "temperatura":
            valor = round(random.uniform(20.0, 50.0), 1) # Entre 20 y 50 grados
        elif tipo_evento == "humo":
            valor = random.choice([0, 1]) # 0: nada, 1: humo detectado
        elif tipo_evento == "movimiento":
            valor = "detectado"
        elif tipo_evento == "puerta":
            valor = random.choice(["abierta", "cerrada"])

        # 3. Crear el mensaje JSON (Estructura solicitada)
        mensaje = {
            "sensor_id": sensor_id,
            "tipo": tipo_evento,
            "valor": valor,
            "timestamp": datetime.now().isoformat()
        }

        # 4. Enviar al Broker
        channel.basic_publish(exchange='', routing_key='alertas_cuenca', body=json.dumps(mensaje))
        
        print(f" [x] Enviado: {mensaje}")
        
        # Esperamos un poco antes del siguiente evento (simulando tiempo real)
        time.sleep(random.uniform(1, 3)) 

except KeyboardInterrupt:
    print("\n Apagando sensores...")
    connection.close()

