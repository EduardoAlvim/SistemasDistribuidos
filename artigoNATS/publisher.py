import asyncio
import nats

async def main():
    # Conecta ao servidor NATS
    nc = await nats.connect("nats://localhost:4222")
    print("Publicador conectado ao NATS.")

    # Envia mensagens de teste a cada 2 segundos
    for i in range(5):
        message = f"Evento número {i+1}"
        await nc.publish("eventos.teste", message.encode())
        print(f"Mensagem publicada: {message}")
        await asyncio.sleep(2)

    # Fecha a conexão
    await nc.drain()

if __name__ == "__main__":
    asyncio.run(main())
