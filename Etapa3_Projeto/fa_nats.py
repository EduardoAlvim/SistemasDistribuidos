import asyncio
import json
from datetime import datetime
from nats.aio.client import Client as NATS

FA_ID = "fa_1"
TOPICO_RESPOSTA = f"mensagens.{FA_ID}"

async def main():
    nc = NATS()
    await nc.connect("nats://localhost:4222")

    # Escutar respostas do palco
    async def resposta_handler(msg):
        data = json.loads(msg.data.decode())
        print(f"[FÃ] Resposta recebida de {data['origem']}: {data['conteudo']}")

    await nc.subscribe(TOPICO_RESPOSTA, cb=resposta_handler)

    # Consultar o endereço do palco no serviço de nomes
    consulta = {"nome": "palco_metallica"}
    response = await nc.request("consulta.nomes", json.dumps(consulta).encode(), timeout=2)
    endereco_palco = json.loads(response.data.decode()).get("endereco")

    if not endereco_palco:
        print("[FÃ] Palco não encontrado no serviço de nomes.")
        return

    print(f"[FÃ] Endereço do palco encontrado: {endereco_palco}")

    # Escutar eventos do palco
    async def evento_handler(msg):
        data = json.loads(msg.data.decode())
        print(f"[FÃ] Evento do {data['origem']}: {data['conteudo']}")

    await nc.subscribe(endereco_palco, cb=evento_handler)

    # Enviar comando ao palco
    comando = {
        "tipo": "comando",
        "origem": FA_ID,
        "destino": "palco_1",
        "conteudo": "To na área, derrubou é pênalti!",
        "timestamp": datetime.now().isoformat()
    }
    await nc.publish("comandos.palco_1", json.dumps(comando).encode())
    print(f"[FÃ] Comando enviado: {comando['conteudo']}")

    # Esperar para continuar recebendo mensagens
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())