import asyncio
import json
from datetime import datetime
from nats.aio.client import Client as NATS

PALCO_ID = "palco_metallica"
TOPICO_EVENTOS = f"eventos.{PALCO_ID}"
TOPICO_COMANDOS = f"comandos.{PALCO_ID}"
TOPICO_RESPOSTA_FA = "mensagens.fa_1"  

# Músicas que tocarão neste palco
setlist = [
    "1. Enter Sandman",
    "2. Master of Puppets",
    "3. Nothing Else Matters",
    "4. One",
    "5. Seek & Destroy"
]

async def main():
    nc = NATS()
    await nc.connect("nats://localhost:4222")

    # Registrar o serviço no serviço de nomes
    registro_msg = {
        "nome": PALCO_ID,
        "endereco": TOPICO_EVENTOS
    }
    await nc.publish("registro.nomes", json.dumps(registro_msg).encode())
    print(f"[PALCO] Registrado como '{PALCO_ID}' no serviço de nomes")

    # Enviar mensagem inicial de boas-vindas
    boas_vindas = {
        "tipo": "evento",
        "origem": PALCO_ID,
        "destino": "todos",
        "conteudo": "🎸 Bem-vindo ao palco METALLICA! O show começará em instantes...",
        "timestamp": datetime.now().isoformat()
    }
    await nc.publish(TOPICO_EVENTOS, json.dumps(boas_vindas).encode())
    await asyncio.sleep(15)  # tempo de espera antes do show

    # Início do show
    comeco_show = {
        "tipo": "evento",
        "origem": PALCO_ID,
        "destino": "todos",
        "conteudo": "🤘 O show começou!",
        "timestamp": datetime.now().isoformat()
    }
    await nc.publish(TOPICO_EVENTOS, json.dumps(comeco_show).encode())

    # Simular setlist
    for musica in setlist:
        evento = {
            "tipo": "evento",
            "origem": PALCO_ID,
            "destino": "todos",
            "conteudo": f"Tocando agora: {musica}",
            "timestamp": datetime.now().isoformat()
        }
        await nc.publish(TOPICO_EVENTOS, json.dumps(evento).encode())
        print(f"[PALCO] {musica}")
        await asyncio.sleep(20)  # tempo fictício por música

    # Fim do show
    fim = {
        "tipo": "evento",
        "origem": PALCO_ID,
        "destino": "todos",
        "conteudo": "🎤 O show acabou! O Metallica agradece vocês!",
        "timestamp": datetime.now().isoformat()
    }
    await nc.publish(TOPICO_EVENTOS, json.dumps(fim).encode())

    print("[PALCO] Show encerrado. Desmontando o palco...")
    await nc.close()

if __name__ == "__main__":
    asyncio.run(main())