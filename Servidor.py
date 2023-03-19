import socket
import ntplib
from time import ctime

NTP_SERVER = "br.pool.ntp.org"
HOST = '192.168.2.7'  # endereço IP do servidor
PORT = 8888  # porta que o servidor estará escutando

# Configuração do cliente NTP
ntp_client = ntplib.NTPClient()

# Configuração do socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)

print(f"Servidor de hora iniciado em {HOST}:{PORT}")

while True:
    conn, addr = sock.accept()
    print(f"Conexão estabelecida com {addr}")
    try:
        # Obtem o horário do servidor NTP
        response = ntp_client.request(NTP_SERVER)
        ntp_time = response.tx_time

        # Converte o horário para uma string formatada
        date_time = ctime(ntp_time)

        # Envia o horário para o cliente
        conn.send(date_time.encode())
    except Exception as e:
        print(f"Erro ao obter horário do servidor NTP: {e}")
    finally:
        conn.close()
