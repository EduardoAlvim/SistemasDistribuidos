import socket         
import threading      
import time           

HOST = 'localhost'    # Endereço do servidor (localhost = máquina local)
PORT = 5050           # Porta onde o servidor vai escutar conexões

# Função que lida com cada fã que se conecta
def handle_fa(conn, addr):
    print(f"[PALCO] Fã conectado: {addr}")  # Log da conexão

    # Envia uma mensagem de boas-vindas ao fã
    conn.sendall("🎸 Bem-vindo ao Palco! O show começa em breve.\n".encode())

    time.sleep(3)  # Espera 3 segundos antes de "iniciar o show"

    # Loop de comunicação com o fã
    while True:
        try:
            data = conn.recv(1024)  # Espera uma mensagem do fã
            if not data:
                break  # Se não recebeu nada, encerra a conexão

            # Exibe a mensagem recebida
            print(f"[PALCO] Mensagem de {addr}: {data.decode().strip()}")

            # Envia uma resposta de volta
            resposta = "🎶 O show começou, ENTRE NO MOSH!"
            conn.sendall(resposta.encode())

        except ConnectionResetError:
            break  # Se o fã fechar a conexão abruptamente, sai do loop

    print(f"[PALCO] Fã desconectado: {addr}")  # Log de desconexão
    conn.close()  # Fecha o socket

# Função principal do servidor
def start_palco():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket TCP
    server.bind((HOST, PORT))  # Associa o socket ao endereço e porta
    server.listen()  # Começa a escutar conexões

    print(f"[PALCO] Servidor iniciado em {HOST}:{PORT}")

    # Aceita conexões continuamente
    while True:
        conn, addr = server.accept()  # Espera por uma nova conexão
        thread = threading.Thread(target=handle_fa, args=(conn, addr))  # Cria nova thread para cada fã
        thread.start()  # Inicia a thread

# Executa o servidor
if __name__ == "__main__":
    start_palco()
