
#GrowLED und Display sind aktiv

from time import sleep
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import urequests
import network
from network import wlan

# Display initialisieren
sda_pin = Pin(0)  # Pin 0 für Daten (SDA)
scl_pin = Pin(1)  # Pin 1 für Takt (SCL)
# SSD1306-Display initialisieren
i2c = I2C(0, sda=sda_pin, scl=scl_pin, freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text("Horst", 0, 8)
oled.show()

def verbinden():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Karl-Popper-Schule","EN9gfcMIDbsw2O2g")
    while not wlan.isconnected() and wlan.status() >= 0:
        print("Verbinde, bitte warten....")
        time.sleep(1)
    print(wlan.ifconfig())
    print("Bin online...")
    return wlan

def update_internetTime():
    response = urequests.get('https://timeapi.io/api/Time/current/zone?timezone=Europe/Berlin')
    print(response.json())
    data= response.json()
    stunden = data['hour']
    minuten = data['minutes']
    sekunden = str(data['seconds'])
                   


wlan = verbinden()
update_internetTime()