import ctypes
import socket
import time

# Configuração do cliente
HOST = 'localhost'
PORT = 12345

# Constantes do algoritmo de Christian
ALPHA = 0.1
BETA = 0.25
ADJUSTMENT_INTERVAL = 10

# Criação do socket do cliente
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Variáveis para o algoritmo de Christian
offset = 0
delay = 0
last_adjustment = 0

# Função para ajustar a hora do sistema Linux
def set_system_time(seconds, microseconds):
    # Define a estrutura timeval com os valores de tempo a serem definidos
    timeval = ctypes.Structure(
        'timeval', 
        [('tv_sec', ctypes.c_long), ('tv_usec', ctypes.c_long)]
    )
    tv = timeval(seconds, microseconds)

    # Chama a função settimeofday do sistema Linux
    libc = ctypes.CDLL('libc.so.6')
    return libc.settimeofday(ctypes.byref(tv), None)

while True:
    # Recebe o horário do servidor
    server_time = float(s.recv(1024).decode())

    # Obtém o horário local
    local_time = time.time()

    # Calcula o delay e o offset
    delay = (time.time() - local_time) / 2
    offset = server_time + delay - local_time

    # Atualiza o horário local gradativamente usando o algoritmo de Christian
    local_time = local_time + ALPHA * offset
    delay = (1 - ALPHA) * delay + ALPHA * abs(offset)

    # Verifica se é hora de ajustar o relógio
    if time.time() - last_adjustment > ADJUSTMENT_INTERVAL:
        # Ajusta o horário em 10 segundos
        local_time += 10
        last_adjustment = time.time()

        # Obtém os segundos e microssegundos a partir do novo horário local
        seconds = int(local_time)
        microseconds = int((local_time - seconds) * 1000000)

        # Chama a função para ajustar a hora do sistema
        set_system_time(seconds, microseconds)

    # Aguarda um segundo antes de atualizar o horário novamente
    time.sleep(1)

    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(local_time)))
