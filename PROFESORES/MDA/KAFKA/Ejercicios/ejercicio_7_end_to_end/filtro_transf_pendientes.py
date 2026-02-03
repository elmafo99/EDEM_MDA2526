import json
from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo-validador-pagos-pendientes', #importante cambiar esto si reutilizamos código para que se muestre por consola
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['transferenciasBancarias'])

print("✅ Filtrando solo transferencias 'Pendiente'...")
print("----------------------------------------------")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        
        # 1. Deserialización
        data = json.loads(msg.value().decode('utf-8'))

        # 2. Lógica de filtrado por estado
        estado = data.get('estado')

        if estado == "Pendiente":
            # Si está pendiente, la mostramos con detalle
            print(f"💰 PAGO PENDIENTE: ID {data['id_transferencia']}")
            print(f"   Monto: {data['monto']} {data['moneda']} | De: {data['pais_origen']}")
            print(f"   Concepto: {data['concepto']}")
            print("-" * 30)
        else:
            # Si está "Completada" o cualquier otro estado, la ignoramos
            # Puedes imprimir un pequeño punto para saber que el script sigue vivo
            print(f"⏳ Ignorando transferencia {data['id_transferencia']} (Estado: {estado})...")

except KeyboardInterrupt:
    print("\nDeteniendo validador...")
finally:
    consumer.close()