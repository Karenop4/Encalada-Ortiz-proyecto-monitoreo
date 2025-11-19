import pika
import json
import time
import requests 

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='alertas_cuenca')

# URL del servidor de tu compañero (Persona 2).
# Por ahora apuntamos a localhost puerto 9000, que es lo que pedía el ejercicio.
URL_DESTINO = "http://localhost:9000/api/alerta"

print("Esperando alertas y reenviando...")

def callback(ch, method, properties, body):
    mensaje_recibido = json.loads(body)
    
  
    tipo = mensaje_recibido["tipo"]
    valor = mensaje_recibido["valor"]
    sensor = mensaje_recibido["sensor_id"]
    
    alerta_procesada = {
        "alerta": "Evento Normal",
        "nivel": "verde", 
        "mensaje": f"Sensor {sensor} operando normalmente",
        "timestamp": mensaje_recibido["timestamp"]
    }

    if tipo == "temperatura":
        if valor > 45:
            alerta_procesada.update({"alerta": "🔥 CALOR CRÍTICO", "nivel": "rojo", "mensaje": f"¡Peligro! {valor}°C en {sensor}"})
        elif valor > 35:
            alerta_procesada.update({"alerta": "⚠️ Advertencia Calor", "nivel": "amarillo", "mensaje": f"Subiendo temp: {valor}°C"})

    elif tipo == "humo" and valor == 1:
        alerta_procesada.update({"alerta": "🚨 INCENDIO DETECTADO", "nivel": "rojo", "mensaje": f"Humo en sensor {sensor}"})

    elif tipo == "puerta" and valor == "abierta":
         alerta_procesada.update({"alerta": "🚪 Puerta Abierta", "nivel": "amarillo", "mensaje": f"Acceso en {sensor}"})

    try:
        # Enviamos el JSON procesado al servidor 
        respuesta = requests.post(URL_DESTINO, json=alerta_procesada)
    
        if respuesta.status_code == 200:
            print(f"✅ Enviado a Websocket: {alerta_procesada['alerta']}")
        else:
            print(f"⚠️ Error al enviar: Servidor respondió {respuesta.status_code}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ No se pudo conectar con el Servidor WebSocket")
        print(f"   --> Dato procesado localmente: {alerta_procesada['alerta']}")

channel.basic_consume(queue='alertas_cuenca', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
