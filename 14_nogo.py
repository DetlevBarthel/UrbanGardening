'''
Zeit zusammen mit Sensordaten und Display. Auch Lampe muss laufen
'''
import sys
import time
import network
import ntptime
import machine
from machine import RTC
import rp2
from machine import Pin, I2C, WDT
from ssd1306 import SSD1306_I2C
import gc # garbge collection
import socket
import struct

# Variablen für den Timer
lock = True
hours= minutes= seconds = 0
# Initialisierung der Echtzeituhr (RTC)
rtc = RTC()
#GMT_OFFSET = 3600 * 1 # 3600 = 1 h (Winterzeit)
GMT_OFFSET = 3600  # 3600 = 1 h (Sommerzeit)
# NTP_HOST = 'pool.ntp.org'
NTP_HOST = 'europe.pool.ntp.org'  # Beispiel für einen alternativen NTP-Server
NTP_DELTA = 2208988800  # Anzahl der Sekunden zwischen 1900 und 1970

# Variablen für das Display
sda_pin = Pin(0)  # Pin 0 für Daten (SDA)
scl_pin = Pin(1)  # Pin 1 für Takt (SCL)
# SSD1306-Display initialisieren
i2c = I2C(0, sda=sda_pin, scl=scl_pin, freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# Variablen für die Grow-LED
grow_ledPin= Pin(15, Pin.OUT)
grow_ledPin.value(0)
current_time = 0
startZeit = 13
endZeit = 14

# Watchdog-Timer Variable initialisiert
wdt = 0

# Temperatur- und Feuchtigkeits-Sensor
import dht
dhtSensor = dht.DHT11(machine.Pin(16))
temp = hum = 0


class Flag:
    run_core_1 = False

    @classmethod
    def set_run_flag(cls):
        cls.run_core_1 = True

    @classmethod
    def clear_run_flag(cls):
        cls.run_core_1 = False

    @classmethod
    def get_run_flag(cls):
        return cls.run_core_1


# Verbindungsfunktion
def verbinden():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect("RoboStudio2GHz", "robo-1958!")
        while not wlan.isconnected():
            pass
    print("Netzwerk konfiguriert:", wlan.ifconfig())



class Timer:
    def __init__():
        
    
    hours = minutes = seconds = 0
    lock = False
       
    def getTimeNTP():
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1B
        addr = socket.getaddrinfo(NTP_HOST, 123)[0][-1]
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.settimeout(5)
            res = s.sendto(NTP_QUERY, addr)
            msg = s.recv(48)
        finally:
            s.close()
        ntp_time = struct.unpack("!I", msg[40:44])[0] - NTP_DELTA + GMT_OFFSET
        return time.localtime(ntp_time)  # Lokalisierte Zeit, keine GMT/UTC

    def setTimeRTC(): # weil diese Methode von der Klassenmethode aufgerufen wird, muss sie selbst keine Klassenmethode sein
        cls.tm = getTimeNTP()  # NTP-Zeit holen
        # Stelle das RTC-Datum ein. tm[6] ist der Wochentag in localtime, 0-basiert mit Montag als 0.
        # Die RTC.datetime-Funktion erwartet jedoch 1-basiert mit Montag als 1, daher tm[6] + 1
        machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
        # Ausgabe der eingestellten Zeit für Überprüfungszwecke
        print("Stunden:", tm[3], "Minuten:", tm[4], "Sekunden:", tm[5])

    # Zeitüberprüfungsfunktion
    def check_and_update_time():
        # Zeit von NTP aktualisieren, wenn es 06:00 Uhr oder 18:00 Uhr ist
        if (cls.hours == 6 or cls.hours == 18) and cls.lock:
            cls.setTimeRTC()
            cls.lock = False
        if cls.hours !=6 or cls.hours != 18:
            cls.lock = True

    

def oled_show():
    oled.fill(0)
    oled.text("Zeit: " + zeit, 0, 0)
    oled.text("Start: " + startZeit,0,8)
    oled.text("Ende:  " + endZeit,0,16)
    oled.text("T:{}C,H:{}%".format(temp, hum), 0, 24)
    free_memory = gc.mem_free()  # Zeige den freien Speicher
    oled.text(str(free_memory), 10, 32)
    oled.show()
    wdt.feed()
    gc.collect()  # Führe Garbage Collection aus
    

# Hauptprogramm
verbinden()  # WLAN verbinden
Timer.setTimeRTC()  # Erstmalige Zeitaktualisierung bei Programmstart

while True:
    Timer.check_and_update_time()  # Überprüfen, ob es Zeit für ein NTP-Update ist
    time.sleep(3)  # Warte eine Stunde vor der nächsten Überprüfung
