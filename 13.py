'''
Die Zeit wird per NTP 2mal täglich geholt und anschliessend intern weitergerechnet 
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

lock = True
hours= minutes= seconds = 0
# Initialisierung der Echtzeituhr (RTC)
rtc = RTC()
#GMT_OFFSET = 3600 * 1 # 3600 = 1 h (Winterzeit)
GMT_OFFSET = 3600  # 3600 = 1 h (Sommerzeit)
# NTP_HOST = 'pool.ntp.org'
NTP_HOST = 'europe.pool.ntp.org'  # Beispiel für einen alternativen NTP-Server

NTP_DELTA = 2208988800  # Anzahl der Sekunden zwischen 1900 und 1970

# Verbindungsfunktion
def verbinden():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect("RoboStudio2GHz", "robo-1958!")
        while not wlan.isconnected():
            pass
    print("Netzwerk konfiguriert:", wlan.ifconfig())

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

# Funktion: RTC-Zeit setzen
def setTimeRTC():
    tm = getTimeNTP()  # NTP-Zeit holen
    # Stelle das RTC-Datum ein. tm[6] ist der Wochentag in localtime, 0-basiert mit Montag als 0.
    # Die RTC.datetime-Funktion erwartet jedoch 1-basiert mit Montag als 1, daher tm[6] + 1
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    # Ausgabe der eingestellten Zeit für Überprüfungszwecke
    print("Stunden:", tm[3], "Minuten:", tm[4], "Sekunden:", tm[5])


# Zeitüberprüfungsfunktion
def check_and_update_time():
    global lock, hours, minutes, seconds
    # Zeit von NTP aktualisieren, wenn es 06:00 Uhr oder 18:00 Uhr ist
    if (hours == 6 or hours == 18) and lock:
        setTimeRTC()
        lock = False
    if hours !=6 or hours != 18:
        lock = True

# Hauptprogramm
verbinden()  # WLAN verbinden
setTimeRTC()  # Erstmalige Zeitaktualisierung bei Programmstart

while True:
    check_and_update_time()  # Überprüfen, ob es Zeit für ein NTP-Update ist
    current_time = rtc.datetime()  # Aktuelle Zeit bekommen
    print("Aktuelle Zeit:", current_time)
    time.sleep(3)  # Warte eine Stunde vor der nächsten Überprüfung
