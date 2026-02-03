import json
from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo-filtro-fiscal',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['transferenciasBancarias'])

# Definimos nuestra "lista negra" de países
paraisos_fiscales = ['Islas Caimán', 'Singapur']

print("🕵️ Monitor de Paraísos Fiscales activo...\n")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        
        # 1. Deserializar
        data = json.loads(msg.value().decode('utf-8'))

        # 2. Lógica de Filtrado
        origen = data.get('pais_origen')
        destino = data.get('pais_destino')

        # Comprobamos si el origen O el destino están en nuestra lista
        if origen in paraisos_fiscales or destino in paraisos_fiscales:
            print(f"🚨 ALERTA - Transacción Sospechosa Detectada:")
            print(f"   ID: {data['id_transferencia']} | Monto: {data['monto']} {data['moneda']}")
            print(f"   Ruta: {origen} ➡️  {destino}")
            print(f"   Concepto: {data['concepto']}")
            print("-" * 40)
        else:
            # Si no es de estos países, no hacemos nada (o ponemos un log silencioso)
            pass

except KeyboardInterrupt:
    print("\nDeteniendo monitor...")
finally:
    consumer.close()