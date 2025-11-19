import asyncio
import json
import websockets

clientes = set()

async def manejar_cliente(websocket):
    clientes.add(websocket)
    print("Cliente conectado")

    try:
        async for mensaje in websocket:
            alerta = json.loads(mensaje)
            await enviar_a_todos(alerta)

    except Exception as e:
        print("Error:", e)

    finally:
        clientes.remove(websocket)
        print("Cliente desconectado")

async def enviar_a_todos(alerta):
    if clientes:
        data = json.dumps(alerta)
        # gather reemplaza a asyncio.wait (no da errores en Python 3.14)
        await asyncio.gather(*(c.send(data) for c in clientes))

async def main():
    async with websockets.serve(manejar_cliente, "0.0.0.0", 9000):
        print("Servidor WebSocket activo en ws://localhost:9000")
        await asyncio.Future()   # servidor corriendo

asyncio.run(main())
