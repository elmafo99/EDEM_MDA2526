from confluent_kafka import Consumer
import json

config = {
    "bootstrap.servers":"localhost:9092",
    "group.id":"consumer_group_paises_estados2",
    "auto.offset.reset":"earliest"
    
}

consumer = Consumer(config)

topic_kafka = "transferencias"
consumer.subscribe([topic_kafka])
print(f"Esperando mensajes del tópico '{topic_kafka}'...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error al recibir mensaje {msg.error()}")
            continue
        message_value = msg.value().decode("utf-8")
        data = json.loads(message_value)
        #print(f"Mensaje recibido: {data}")

        estado = data.get("estado")
        pais = data.get("pais_origen")
        monto = data.get("monto")
        
        if estado == "Pendiente":
            print(f"Transferencia pendiente desde {pais} por un monto de {monto}")
        else:
            print(f"Ignorando... Transferencia con estado {estado}")       
        
except KeyboardInterrupt:
    print("Programa detenido por el usuario")

finally:
    consumer.close()