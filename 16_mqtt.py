# installiere umqtt.robust
# installiere umqtt.simple
import network
from machine import Pin
import utime
from time import sleep
import dht
dhtSensor = dht.DHT11(machine.Pin(16))
from umqtt.simple import MQTTClient

def verbinden():
    
    rp2.country("DE") # Jedes Land hat andere Vorschiften für das W-Lan (z.B. Signalstärke, verfügbare Kanäle) und stellt diese entsprechend ein. Ist aber optional.
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Gr.Hasenpfad_2.4", "robo-1958!")
    
    # Der Aufbau einer Verbindung dauert eine Weile und es werden unterumständen mehrer Versuche benötigt bis eine Verbindung hergestellt wurde.
    while not wlan.isconnected() and wlan.status() >= 0:
        print("Verbinde, bitte warten...")
        time.sleep(2) # Pause zwische 2 Verbindungsversuche
        
    print(wlan.ifconfig())
    print("Bin online...")
    return wlan

# user von hivemq.com angelegt
# Name für serverless account: detlev.barthel, pw: Robo-1958"
def connectMQTT():
    client = MQTTClient(client_id="pico_W_1",
                        server= b"bde1be3a9e954388b08a9aafcbda674a.s1.eu.hivemq.cloud",
                        port=0,
                        user="detlev.barthel",
                        password=b"Robo-1958!",
                        keepalive= 7200,
                        ssl=True,
                        )
    
def publish(topic, value):
    print(topic)
    print(value)
    client.publish(topic, value)
    print("publishing done")
    

verbinden()
client = connectMQTT()
    
while True:
    pass
    #sensor_reading = 


