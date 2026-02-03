import json
from confluent_kafka import Consumer, KafkaError

# 1. Configuración del Consumidor
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo-analisis-bancario', # se crea un consumer group formado por varias máquinas para que lea los mensajes (se reparten los mensajes)
    'auto.offset.reset': 'earliest' # Lee desde el principio si es un grupo nuevo
}

consumer = Consumer(conf)
topic = 'transferenciasBancarias'
consumer.subscribe([topic])

print(f"Escuchando transferencias en el tópico: {topic}...\n")

try:
    while True:
        msg = consumer.poll(1.0) # Espera 1 segundo por mensajes

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Error: {msg.error()}")
                break

        # --- AQUÍ OCURRE LA DESERIALIZACIÓN ---
        # 1. Decodificamos los bytes a string (utf-8)
        raw_value = msg.value().decode('utf-8')
        
        # 2. Convertimos el string JSON a un diccionario de Python
        transferencia = json.loads(raw_value)

        # Ahora podemos acceder a los datos como un objeto de Python
        id_tx = transferencia.get('id_transferencia')
        monto = transferencia.get('monto')
        pais = transferencia.get('pais_origen')
        estado = transferencia.get('estado')

        print(f"✅ [NUEVO MENSAJE] ID: {id_tx} | Origen: {pais} | Monto: {monto}€ | Estado: {estado}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()