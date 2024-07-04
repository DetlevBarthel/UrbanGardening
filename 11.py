# wir checken, ob der Watchdog timer den Pico nicht nur aus, sondern auch anschaltet
# Der Watchdog-Timer funktioniert natürlich nur dann richtig, wenn die auszuführende Datei
# als main.py auf dem Pico gespeichert wird. Dann startet sie tatsächlich das Board nach einem Reboot
# von Neuem

import time
import urequests
from machine import Pin, I2C, WDT
from ssd1306 import SSD1306_I2C
import gc

# Display initialisieren
sda_pin = Pin(0)  # Pin 0 für Daten (SDA)
scl_pin = Pin(1)  # Pin 1 für Takt (SCL)
# SSD1306-Display initialisieren
i2c = I2C(0, sda=sda_pin, scl=scl_pin, freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

print("Hallo 1")

wdt = 0
wdt = WDT(timeout=2000)  # enable it with a timeout of 2s - must be feed within 2 seconds constantly!

while True:
    
    if time.ticks_ms() < 10000:
        wdt.feed()
    oled.fill(0)
    oled.text(str(time.ticks_ms()),0,28)
    oled.show()



    


