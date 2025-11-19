import asyncio
import websockets
import json
import time

async def enviar():
    async with websockets.connect("ws://localhost:9000") as ws:
        for i in range(5):
            alerta = {
                "alerta": f"Prueba {i+1}",
                "nivel": "amarillo",
                "mensaje": f"Mensaje de prueba {i+1}",
                "sensor_id": f"S-{100+i}",
                "timestamp": "2025-11-19T14:03:52Z"
            }
            await ws.send(json.dumps(alerta))
            print(f"Mensaje {i+1} enviado")
            time.sleep(1)  # espera 1 segundo entre mensajes

asyncio.run(enviar())
