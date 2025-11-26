import socket
import struct
import os

HOST = '10.25.1.162'
PORT = 60000

FILE_NAME = "teste.txt"

def send_file(s, addr, file_name):
    bytes_sent = 0
    with open(file_name, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            s.sendto(data, addr)
    print(f"Arquivo {file_name} enviado com sucesso.")

#try:
#    with open(FILE_NAME, "w") as f:
#        f.write("Arquivo de teste para download.")
#except IOError as e:
#    print(f"Falha ao salvar o arquivo: {e}")
#    exit(1)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))

    print(f"Aceitando conexões em {HOST}:{PORT}")
    while True:
        try:
            file_length_data, addr = s.recvfrom(1)
            file_name_length = struct.unpack('>B', file_length_data)[0]

            file_name_data, _ = s.recvfrom(file_name_length)
            file_name = file_name_data.decode()

            print(f"Arquivo solicitado: {file_name}")

            if file_name != "teste.txt":
                status = struct.pack('>B', 0)
                s.sendto(status, addr)

            status = struct.pack('>B', 1)
            s.sendto(status, addr)
            print(f"Arquivo encontrado: {FILE_NAME}")

            file_size = os.path.getsize(FILE_NAME)
            print(f"Tamanho do arquivo: {file_size} bytes")

            size_bytes = struct.pack('>I', file_size)
            s.sendto(size_bytes, addr)

            send_file(s, addr, FILE_NAME)
        except socket.timeout:
            print("Timeout ao aguardar dados do cliente.")
            continue
        except UnicodeDecodeError as e:
            print(f"Erro ao decodificar nome do arquivo: {e}")
            try:
                status = struct.pack('>B', 1)
                s.sendto(status, addr)
            except:
                pass
            continue
            
