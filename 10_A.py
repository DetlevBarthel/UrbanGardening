'''
Links ist der Datenausgang, Mitte 3.3v, rechts Erde, ganz anders als in vielen
Bildern dargestellt.
'''
import dht
import machine
import time
import json
sensor = dht.DHT11(machine.Pin(16))
def read_sensor_data():
    try:
        sensor.measure()  # Starte Messung
        temp = sensor.temperature()  # Temperatur auslesen
        hum = sensor.humidity()  # Luftfeuchtigkeit auslesen
        #timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # Aktuellen Zeitstempel generieren

        # Erstelle JSON-Objekt mit den Sensorwerten und dem Zeitstempel
        data = {
            "timestamp": "timestamp",
            "temperature": temp,
            "humidity": hum
        }

        return data

    except Exception as e:
        print("Fehler beim Auslesen des Sensors:", e)
        return None
while True:
    sensor_data = read_sensor_data()
    if sensor_data:
        print(sensor_data)
    time.sleep(2)  # Warte 2 Sekunden bis zur nächsten Messung
