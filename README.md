# Centro de Control de Alertas Industriales - Cuenca

Este proyecto implementa un sistema de monitoreo en tiempo real de sensores industriales para la ciudad de Cuenca. Utiliza **RabbitMQ**, **Python**, y **WebSockets** para recibir, procesar y mostrar alertas en un **dashboard web**.

---

## Estructura del Proyecto

Encalada-Ortiz-proyecto-monitoreo/
│
├── sensores/                 # Productores de mensajes (sensores simulados)

│   ├── productor_sensor.py

│   └── Dockerfile

│

├── consumidores/             # Procesador de alertas

│   ├── procesador_alertas.py

│   └── Dockerfile

│

├── websocket_server/         # Servidor WebSocket

│   └── ws_server.py

│

├── web_client/               # Cliente web (dashboard)

│   ├── index.html

│   └── styles.css

│

├── docker-compose.yml        # Configuración de Docker

└── README.md

---

##  Requisitos

- Python 3.14 (para scripts locales)
- Docker y Docker Compose (para contenedores)
- Navegador moderno (Chrome, Edge, Firefox)

---

## Ejecutar el proyecto

1. En la terminal de comandos nos dirigimos a la carpeta del proyecto
2. Usamos el comando docker-compose up --build


##  Dashboard Web (Cliente WebSocket)

1. Abre `web_client/index.html` en tu navegador.
2. El dashboard recibirá automáticamente todas las alertas procesadas.
3. Las alertas se muestran en **tarjetas** codificadas por color:
   - **Rojo**: crítico
   - **Amarillo**: advertencia
   - **Verde**: normal
4. Información mostrada:
   - Tipo de alerta
   - Mensaje descriptivo
   - Sensor
   - Timestamp

---

##  Configuración WebSocket

- Servidor WebSocket (`ws_server.py`) escucha en:

ws://localhost:9000

- Todos los clientes conectados recibirán alertas en tiempo real.

---

##  Dependencias Python

Instalar las dependencias necesarias:

pip install pika requests websockets

> Asegúrate de tener la versión correcta de Python (3.14) para evitar errores de compatibilidad.

---

## Flujo del Sistema

1. **Sensores simulados** envían datos a RabbitMQ (`alertas_cuenca`).
2. **Procesador de alertas** consume los datos, los clasifica y envía JSON al servidor WebSocket.
3. **Servidor WebSocket** distribuye las alertas a todos los clientes conectados.
4. **Dashboard web** muestra las alertas en tiempo real con colores y detalles de cada sensor.

---

## Notas

- No se cambia la lógica del sistema al mejorar la interfaz web.
- Los contenedores Docker comparten una red interna (`red_cuenca`) para comunicarse con RabbitMQ.
- Para desarrollo local, usar `localhost` como host para conectar a RabbitMQ y WebSocket.

---

## Mejoras posibles

- Agregar iconos por tipo de alerta.
- Reproducir un sonido para alertas críticas.
- Contador de eventos por tipo de sensor.
- Historial de alertas en la interfaz web.

---

Creado como proyecto académico de monitoreo industrial.
