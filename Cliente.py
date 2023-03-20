import socket
import time 
from datetime import datetime
import subprocess

HOST = '192.168.3.148'  # endereço IP do servidor
PORT = 3000  # porta em que o servidor está escutando

# Configuração do socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Tempo de ajuste
ADJUST_TIME = 10  # segundos

while True:
    # Recebe o horário do servidor
    server_time_str = sock.recv(1024).decode()
    server_time = time.strptime(server_time_str,"%Y-%m-%d %H: %M: %S")

    # Calcula a diferença de tempo
    diff = server_time - time.time()

    # Ajusta o relógio gradualmente
    for i in range(ADJUST_TIME):
        
        new_time = time.time() + diff/ADJUST_TIME
        new_time_str = time.starftime("%Y-%m-%d %H: %M: %S", new_time)        
        subprocess.call(["timedatactl","set-ntp","false"])
        subprocess.call(["sudo","timedatectl","set-time",new_time_str])
        subprocess.call(["sudo","hwclock","--systohc"])
        print(f"Horário ajustado para: {new_time}")
        time.sleep(1)

sock.close()
