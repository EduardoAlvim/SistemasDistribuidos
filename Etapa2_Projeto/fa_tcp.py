import socket  
import time    

HOST = 'localhost'  # Endereço do servidor (palco)
PORT = 5050         # Porta do servidor

# Função principal que conecta ao palco
def fa_connecta():
    # Cria um socket TCP dentro de um contexto (com 'with' ele será fechado automaticamente)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))  # Conecta-se ao servidor
        print("[FÃ] Conectado ao palco.")

        # Recebe e imprime a mensagem de boas-vindas do palco
        mensagem = sock.recv(1024).decode()
        print(f"[FÃ] Recebido: {mensagem}")

        # Envia a primeira mensagem para o palco
        sock.sendall("To na área, derrubou é pênalti!".encode())

        # Recebe a resposta do palco
        resposta = sock.recv(1024).decode()
        print(f"[FÃ] Resposta do palco: {resposta}")

        time.sleep(10)  # Aguarda 10 segundos para simular tempo passado no show

        # Envia mensagem final antes de encerrar
        sock.sendall("Obrigado pelo show!".encode())

# Executa o fã
if __name__ == "__main__":
    fa_connecta()
