import asyncio
import nats

async def message_handler(msg):
    subject = msg.subject
    data = msg.data.decode()
    print(f"Mensagem recebida em '{subject}': {data}")

async def main():
    # Conecta ao servidor NATS
    nc = await nats.connect("nats://localhost:4222")
    print("Assinante conectado ao NATS.")

    # Inscreve-se no canal "eventos.teste"
    await nc.subscribe("eventos.teste", cb=message_handler)

    # Mantém o programa rodando para ouvir as mensagens
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
