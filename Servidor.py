import socket
import ntplib
import time

# Configuração do servidor
HOST = 'localhost'
PORT = 12345

# Conexão com o servidor NTP
ntp_client = ntplib.NTPClient()
ntp_server = 'br.pool.ntp.org'

# Criação do socket do servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

while True:
    # Aguarda conexão com um cliente
    conn, addr = s.accept()
    print('Conectado por', addr)

    while True:
        # Obtém o horário do servidor NTP
        response = ntp_client.request(ntp_server)
        server_time = response.tx_time

        # Envia o horário para o cliente
        conn.sendall(str(server_time).encode())

        # Aguarda 5 segundos antes de atualizar o horário novamente
        time.sleep(5)
