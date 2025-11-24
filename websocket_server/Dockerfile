FROM python:3.9-slim
WORKDIR /app
RUN pip install websockets
COPY . .
CMD ["python", "-u", "ws_server.py"]