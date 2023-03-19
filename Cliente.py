import socket
import datetime
from time import sleep
from datetime import datetime, timedelta

HOST = '192.168.2.7'  # endereço IP do servidor
PORT = 8888  # porta em que o servidor está escutando

# Configuração do socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Tempo de ajuste
ADJUST_TIME = 10  # segundos


def update_system_time(timestamp):
    """
    Atualiza o relógio do sistema com o timestamp Unix fornecido.
    """
    # Cria um objeto datetime a partir do timestamp
    dt = datetime.datetime.fromtimestamp(timestamp)

    # Obtém a data e hora em um formato de string
    date_str = dt.strftime('%Y-%m-%d')
    time_str = dt.strftime('%H:%M:%S')

    # Define a data e hora do sistema
    import os
    os.system(f'date {date_str}')
    os.system(f'time {time_str}')


while True:
    # Recebe o horário do servidor
    server_time_str = sock.recv(1024).decode()
    server_time = datetime.strptime(server_time_str, "%a %b %d %H:%M:%S %Y")

    # Calcula a diferença de tempo
    diff = server_time - datetime.now()

    # Ajusta o relógio gradualmente
    for i in range(ADJUST_TIME):
        new_time = datetime.now() + diff/ADJUST_TIME
        # Ajusta o relógio local do cliente
        adjusted_time = time.time() + time_diff

        # Atualiza o relógio do sistema
        update_system_time(adjusted_time)
        print(f"Horário ajustado para: {new_time}")
        sleep(1)
    sleep(3)

sock.close()
