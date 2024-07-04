import network
import ntptime
import machine
import time
from machine import RTC

# Initialisierung der Echtzeituhr (RTC)
rtc = RTC()

# Verbindungsfunktion
def verbinden():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect("IhrWLAN", "IhrPasswort")
        while not wlan.isconnected():
            pass
    print("Netzwerk konfiguriert:", wlan.ifconfig())

# NTP-Zeitaktualisierungsfunktion
def update_time_from_ntp():
    ntptime.settime()  # NTP-Zeitaktualisierung
    print("Zeit aktualisiert von NTP")

# Zeitüberprüfungsfunktion
def check_and_update_time():
    current_time = rtc.datetime()  # Aktuelle Zeit von der RTC bekommen
    current_hour = current_time[4]  # Stunden der aktuellen Zeit
    # Zeit von NTP aktualisieren, wenn es 06:00 Uhr oder 18:00 Uhr ist
    if current_hour == 6 or current_hour == 18:
        update_time_from_ntp()

# Hauptprogramm
verbinden()  # WLAN verbinden
update_time_from_ntp()  # Erstmalige Zeitaktualisierung bei Programmstart

while True:
    check_and_update_time()  # Überprüfen, ob es Zeit für ein NTP-Update ist
    current_time = rtc.datetime()  # Aktuelle Zeit bekommen
    print("Aktuelle Zeit:", current_time)
    time.sleep(3600)  # Warte eine Stunde vor der nächsten Überprüfung
