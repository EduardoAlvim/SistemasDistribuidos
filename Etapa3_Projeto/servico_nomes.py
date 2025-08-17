import asyncio
import json
from nats.aio.client import Client as NATS

# Dicionário para armazenar registros de serviços
servicos_registrados = {}

async def main():
    nc = NATS()
    await nc.connect("nats://localhost:4222")

    async def registro_handler(msg):
        data = json.loads(msg.data.decode())
        nome = data.get("nome")
        endereco = data.get("endereco")
        if nome and endereco:
            servicos_registrados[nome] = endereco
            print(f"[REGISTRO] Serviço '{nome}' registrado em {endereco}")

    async def consulta_handler(msg):
        data = json.loads(msg.data.decode())
        nome = data.get("nome")
        resposta = {"nome": nome, "endereco": servicos_registrados.get(nome)}
        await nc.publish(msg.reply, json.dumps(resposta).encode())
        print(f"[CONSULTA] Serviço '{nome}' consultado → {resposta['endereco']}")

    await nc.subscribe("registro.nomes", cb=registro_handler)
    await nc.subscribe("consulta.nomes", cb=consulta_handler)

    print("[SERVIÇO DE NOMES] Pronto e escutando em 'registro.nomes' e 'consulta.nomes'...")
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())