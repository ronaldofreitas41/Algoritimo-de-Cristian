import socket
from time import sleep
from datetime import datetime, timedelta

HOST = '192.168.2.7'  # endereço IP do servidor
PORT = 8888  # porta em que o servidor está escutando

# Configuração do socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Tempo de ajuste
ADJUST_TIME = 10  # segundos

while True:
    # Recebe o horário do servidor
    server_time_str = sock.recv(1024).decode()
    server_time = datetime.strptime(server_time_str, "%a %b %d %H:%M:%S %Y")

    # Calcula a diferença de tempo
    diff = server_time - datetime.now()

    # Ajusta o relógio gradualmente
    for i in range(ADJUST_TIME):
        new_time = datetime.now() + diff/ADJUST_TIME
        print(f"Horário ajustado para: {new_time}")
        sleep(1)

sock.close()
