import time
import json
from json import dumps
from confluent_kafka import Producer

config = {
    "bootstrap.servers":"localhost:9092",
    "client.id":"python_producer"

}

producer = Producer(config)

topic_kafka = "transferencias"

try:
    with open('transferencias.txt', 'r', encoding='utf-8') as file:
        for linea in file:
            linea = linea.strip()
            if not linea:
                continue
            
            transferencia = json.loads(linea)
            data_str = dumps(transferencia, ensure_ascii=False)
            
            producer.produce(
                topic=topic_kafka,
                key=str(transferencia["id_transferencia"]),
                value=data_str.encode('utf-8')
            )
            producer.poll(0)  # Procesa eventos de entrega (callbacks) sin bloquear
            
            print(f"Enviando datos: {data_str} al tópico {topic_kafka}")
            
            time.sleep(1)
except:
    print("Error al leer el archivo de transferencias.")
    exit(1)
    
pending=producer.flush()
if pending!=0:
    print(f"Quedan {pending} mensajes sin enviar")