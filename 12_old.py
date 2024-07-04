# mit dem dht11 temperatur und luftfeuchte auslesen

import network
import time
import rp2
import urequests
from machine import Pin, I2C, WDT
from ssd1306 import SSD1306_I2C
import gc
#   neu
import dht
dhtSensor = dht.DHT11(machine.Pin(16))

# Display initialisieren
sda_pin = Pin(0)  # Pin 0 für Daten (SDA)
scl_pin = Pin(1)  # Pin 1 für Takt (SCL)
# SSD1306-Display initialisieren
i2c = I2C(0, sda=sda_pin, scl=scl_pin, freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

grow_ledPin= Pin(15, Pin.OUT)
grow_ledPin.value(0)
current_time = 0
startZeit = '13:00'
endZeit = '13:01'
wdt = 0


def verbinden():
    global wdt
    rp2.country("DE") # Jedes Land hat andere Vorschiften für das W-Lan (z.B. Signalstärke, verfügbare Kanäle) und stellt diese entsprechend ein. Ist aber optional.
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("RoboStudio2GHz", "robo-1958!")
    
    # Der Aufbau einer Verbindung dauert eine Weile und es werden unterumständen mehrer Versuche benötigt bis eine Verbindung hergestellt wurde.
    while not wlan.isconnected() and wlan.status() >= 0:
        print("Verbinde, bitte warten...")
        time.sleep(1) # Pause zwische 2 Verbindungsversuche
        
    print(wlan.ifconfig())
    print("Bin online...")
    wdt = WDT(timeout=4000)  # enable it with a timeout of 2s - must be feed within 2 seconds constantly!
    return wlan

def update_internetTime():
    global current_time, startZeit, endZeit, wdt
    # Uhrzeit von API abrufen    
    response = urequests.get('https://timeapi.io/api/Time/current/zone?timezone=Europe/Berlin')
    #print(response)
    while response.status_code != 200:
        response = urequests.get('https://timeapi.io/api/Time/current/zone?timezone=Europe/Berlin')
        time.sleep(1)
        print("Fehler beim Abrufen der Uhrzeit:", response.status_code)
        response.close()
    if response.status_code == 200:
        # JSON-Daten von der API abrufen
        data = response.json()
        # Uhrzeit aus den JSON-Daten extrahieren
        current_time = data['time']
        #print(type(data['time']))
        sekunden = str(data['seconds'])
        zeit = current_time+":"+sekunden
        # Uhrzeit auf Display schreiben
        oled.fill(0)
        oled.text("Zeit: " + zeit, 0, 0)
        oled.text("Start: " + startZeit,0,8)
        oled.text("Ende:  " + endZeit,0,16)
        
        wdt.feed()
        gc.collect()  # Führe Garbage Collection aus
        show_memory()  # Zeige den freien Speicher
        oled.show()
#   neu
def read_temperature():
    try:
        dhtSensor.measure()
        temp = dhtSensor.temperature()  # Temperatur in Celsius
        hum = dhtSensor.humidity()  # Luftfeuchtigkeit in Prozent
        
        print("Temperatur: {}°C, Luftfeuchtigkeit: {}%".format(temp, hum))
        oled.text("Temp: {}C".format(temp), 0, 24)
        oled.text("Hum: {}%".format(hum), 0,32)
        
        
    except OSError as e:
        print("Fehler beim Lesen vom DHT11-Sensor: ", e)




def show_memory():
    free_memory = gc.mem_free()
    oled.text("Free: ", 0, 40)
    oled.text(str(free_memory), 30, 48)
    

def grow_led():
    print(current_time)
    if current_time == startZeit and grow_ledPin.value()==0:
        grow_ledPin.value(1)
    if current_time ==endZeit and grow_ledPin.value()==1:
        grow_ledPin.value(0)
    
wlan = verbinden()
while True:
        #  neu
    read_temperature()
    #time.sleep(1)
    update_internetTime()
    grow_led()





    


