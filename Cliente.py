import socket
import time
from datetime import datetime
import datetime as dt
import subprocess

HOST = '192.168.5.60'  # endereço IP do servidor
PORT = 123  # porta em que o servidor está escutando

# Configuração do socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Tempo de ajuste
ADJUST_TIME = 10  # segundos

while True:
    # Recebe o horário do servidor
    server_time_str = sock.recv(1024).decode()
    server_time = datetime.strptime(server_time_str, '%a %b %d %H:%M:%S %Y')

    # Calcula a diferença de tempo
    diff = server_time - datetime.now()

    # Ajusta o relógio gradualmente
    cont = 0
    while diff.total_seconds() > cont:
        cont += ADJUST_TIME
        new_time = datetime.now() + dt.timedelta(seconds=ADJUST_TIME)
        new_time_str = new_time.strftime('%Y-%m-%d %H:%M:%S')
        # atualiza a hora do sistema
        subprocess.run(["date", "-s", new_time_str])
        print(f"Horário ajustado para: {new_time}")
        time.sleep(1)

    # Aguarda novo ajuste
    time.sleep(ADJUST_TIME)

sock.close()