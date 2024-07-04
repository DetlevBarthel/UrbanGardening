from machine import Pin
import utime as time
from time import sleep
from dht import DHT11
# Initialisieren des DHT11-Sensors
dataPin = 16
myPin = Pin(dataPin, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(myPin)
time.sleep(1)
def read_temperature():
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        # Daten auf der immer gleichen Zeile darstellen
        # im Print-Befehl "\r", voranstellen, am Ende schreibst Du end=''
        print("Temperatur: {}°C, Luftfeuchtigkeit: {}%".format(temp, hum))
        time.sleep(1)
        #return temp, hum
    except OSError as e:
        print("Fehler beim Lesen vom DHT11-Sensor: ", e)
        return None, None

# Hauptschleife
while True:
    #temp, hum = read_temperature()
    read_temperature()
    #if temp is not None and hum is not None:
        # Veröffentlichen Sie die Werte oder führen Sie andere Aktionen durch
    #   pass
    sleep(5)
