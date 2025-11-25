import struct
import os

HOST = '127.0.0.1'
PORT = 60000

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    file_name = input("Informe o nome do arquivo para download: ")
    if not file_name:
        print("Informe um nome!")
        exit(1)

    file_name_length = len(file_name)

    # Verifica se o nome não ultrapassa 1 byte
    if file_name_length > 255:
        print("O nome do arquivo é muito longo (máximo de 255 caracteres)!")
        exit(1)

    fl_bytes = struct.pack('>B', file_name_length)
    s.sendto(fl_bytes, (HOST, PORT))

    fn_bytes = file_name.encode('utf-8')
    s.sendto(fn_bytes, (HOST, PORT))

    print(f"Arquivo soolicitado: {file_name}")
