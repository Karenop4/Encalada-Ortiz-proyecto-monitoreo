import asyncio
import json
import websockets

# Escuchamos en todas las interfaces (0.0.0.0) puerto 9000
HOST = '0.0.0.0'
PORT = 9000

clientes = set()

async def manejar_cliente(websocket):
    # 1. Registrar nuevo cliente (Navegador o Procesador)
    clientes.add(websocket)
    print(f" Nuevo cliente conectado. Total: {len(clientes)}")

    try:
        # 2. Escuchar mensajes entrantes
        async for mensaje in websocket:
            await enviar_a_todos(mensaje)

    except websockets.exceptions.ConnectionClosed:
        pass 
    finally:
        # 3. Limpieza al desconectar
        clientes.remove(websocket)
        print(f" Cliente desconectado. Total: {len(clientes)}")

async def enviar_a_todos(mensaje):
    if clientes:
        websockets_activos = [cliente.send(mensaje) for cliente in clientes]
        await asyncio.gather(*websockets_activos)

async def main():
    print(f" Servidor WebSocket iniciando en ws://{HOST}:{PORT}")
    async with websockets.serve(manejar_cliente, HOST, PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
