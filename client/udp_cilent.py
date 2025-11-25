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

    try:
        status_data, addr = s.recvfrom(1)
    except s.timeout:
        print("ERRO: tempo de espera excedido.")
        exit(1)
    except s.ConnectionRefusedError:
        print("ERRO: Conexão perdida: porta inacessiva")

    status = struct.unpack('>B', status_data)[0]
    
    if status == 0:
        print("Arquivo não existe.")
    elif status == 1:
        print("Arquivo encontrado! Iniciando o download.")
    else:
        print("Erro durante a requisição do nome de arquivo.")
    
    try:
        size_file, addr = s.recvfrom(4)
    except s.timeout:
        print("ERRO: tempo de espera excedido.")
    except s.ConnectionRefusedError:
        print("ERRO: Conexão perdida: porta inacessiva")

        if size_file != 4:
            print("tamanho de arquivo inválido.")
            exit(1)
        
        sf_length = struct.unpack('>I', size_file)[0]
