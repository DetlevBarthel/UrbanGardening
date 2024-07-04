# Diese Programm verbindet den Pico W mit einem W-Lan.
# Verbindung zur Zeit-API

import network
import time
import urequests

def verbinden():
    #rp2.country("DE") # Jedes Land hat andere Vorschiften für das W-Lan (z.B. Signalstärke, verfügbare Kanäle) und stellt diese entsprechend ein. Ist aber optional.
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Robo-Studio_2.4", "Router-1958!")
    
    # Der Aufbau einer Verbindung dauert eine Weile und es werden unterumständen mehrer Versuche benötigt bis eine Verbindung hergestellt wurde.
    while not wlan.isconnected() and wlan.status() >= 0:
        print("Verbinde, bitte warten...")
        time.sleep(1) # Pause zwische 2 Verbindungsversuche
        
    print(wlan.ifconfig())
    print("Bin online...")
    return wlan

def update_internetTime():
    # Uhrzeit von API abrufen    
    response = urequests.get('https://timeapi.io/api/Time/current/zone?timezone=Europe/Berlin')
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
        stunden = data['hour']
        minuten = data['minute']
        sekunden = data['seconds']
        sekunden = str(data['seconds'])
        zeit = current_time+":"+sekunden
        print(current_time)
        print(data)
  

wlan = verbinden()

update_internetTime()

    