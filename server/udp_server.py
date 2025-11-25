import socket
import struct
import os

HOST = '127.0.0.1'
PORT = 60001

FILE_NAME = "teste.txt"

try:
    with open(FILE_NAME, "w") as f:
        f.write("Arquivo de teste para download.")
except IOError as e:
    print(f"Falha ao salvar o arquivo: {e}")
    exit(1)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))

    print(f"Aceitando conexões em {HOST}:{PORT}")
    while True:
        try:
            file_name_bytes, addr = s.recvfrom(1)
            file_name_length = struct.unpack('>B', file_name_bytes)[0]

            file_name_bytes, _ = s.recvfrom(file_name_length)
            file_name = file_name_bytes.decode('utf-8')

            print(f"Arquivo solicitado: {file_name}")

            if file_name != "teste.txt":
                status = struct.pack('>B', 1)
                s.sendto(status, addr)

            status = struct.pack('>B', 0)
            s.sendto(status, addr)
            print(f"Arquivo encontrado: {FILE_NAME}")

            file_size = os.path.getsize(FILE_NAME)
            print(f"Tamanho do arquivo: {file_size} bytes")

            size_bytes = struct.pack('>I', file_size)
            s.sendto(size_bytes, addr)
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
