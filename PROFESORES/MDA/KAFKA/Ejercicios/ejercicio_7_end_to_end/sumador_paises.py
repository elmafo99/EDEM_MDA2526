import json
from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'grupo-contable',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['transferenciasBancarias'])

# Diccionario para guardar los totales: {'Pais': SumaTotal}
acumulado_por_pais = {}

print("📊 Calculando totales por país en tiempo real...")
print("Presiona Ctrl+C para ver el informe final o detener.\n")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        
        # 1. Deserializar
        data = json.loads(msg.value().decode('utf-8'))
        
        pais = data.get('pais_origen')
        monto = data.get('monto')

        # 2. Lógica de acumulación
        if pais in acumulado_por_pais:
            acumulado_por_pais[pais] += monto
        else:
            acumulado_por_pais[pais] = monto

        # 3. Mostrar progreso en consola
        print(f"📥 Procesado: {pais} (+{monto})")
        
        # Opcional: Mostrar tabla resumen cada vez que llega un mensaje
        print("\n--- RESUMEN ACTUALIZADO ---")
        for p, total in acumulado_por_pais.items():
            print(f"📍 {p}: {total:,.2f} EUR")
        print("---------------------------\n")

except KeyboardInterrupt:
    print("\n\n📉 INFORME FINAL DE TRANSFERENCIAS:")
    for p, total in acumulado_por_pais.items():
        print(f"💰 {p}: {total:,.2f} EUR")
    print("\nCerrando...")
finally:
    consumer.close()