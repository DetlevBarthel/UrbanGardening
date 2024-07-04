import network
from machine import Pin
import utime
from time import sleep
import dht
import ssl as ssl  # Importieren Sie das SSL-Modul
from umqtt.simple import MQTTClient

dhtSensor = dht.DHT11(Pin(16))
temp = hum = 0

def verbinden():
    rp2.country("DE")  # Jedes Land hat andere Vorschiften für das W-Lan (z.B. Signalstärke, verfügbare Kanäle) und stellt diese entsprechend ein. Ist aber optional.
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Gr.Hasenpfad_2.4", "robo-1958!")
    
    # Der Aufbau einer Verbindung dauert eine Weile und es werden unterumständen mehrer Versuche benötigt bis eine Verbindung hergestellt wurde.
    while not wlan.isconnected() and wlan.status() >= 0:
        print("Verbinde, bitte warten...")
        sleep(2)  # Pause zwischen 2 Verbindungsversuche
    
    print(wlan.ifconfig())
    print("Bin online...")
    return wlan

def connectMQTT():
    client = MQTTClient(client_id="pico_W_1",
                        server="bde1be3a9e954388b08a9aafcbda674a.s1.eu.hivemq.cloud",
                        port=8883,
                        user="detlev.barthel",
                        password="Robo-1958!",
                        keepalive=7200,
                        ssl=True)
    client.connect()
    return client

def publish(client, topic, value):
    print(topic)
    print(value)
    client.publish(topic, value)
    print("publishing done")

def read_temperature():
    global temp, hum
    try:
        dhtSensor.measure()
        temp = dhtSensor.temperature()  # Temperatur in Celsius
        hum = dhtSensor.humidity()  # Luftfeuchtigkeit in Prozent
        print("Temperatur: {}°C, Luftfeuchtigkeit: {}%".format(temp, hum))
    except OSError as e:
        print("Fehler beim Lesen vom DHT11-Sensor: ", e)

# Verbinden mit dem WLAN
verbinden()

# MQTT-Client verbinden
client = connectMQTT()

# Hauptschleife
while True:
    read_temperature()
    publish(client, 'PicoW/temp', str(temp))  # Temperatur veröffentlichen
    publish(client, 'PicoW/hum', str(hum))    # Luftfeuchtigkeit veröffentlichen
    sleep(5)
