import machine
import urequests as requests
import network
import time
ssid = 'Robo-Studio_2.4G'
pw = 'robo-1958!'
#import constants


def connect_to_wifi(ssid, psk):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, psk)

    #while not wlan.isconnected() and wlan.status() >= 0:
    while not wlan.isconnected():
        wlan.active(True)
        wlan.connect(ssid, psk)
        print("Waiting to Connect")
        time.sleep(2)
    if not wlan.isconnected():
        raise Exception("Wifi not available")
    print("Connected to WiFi")


try:
    connect_to_wifi(ssid, pw)
    # Need to substitute from DATA API
    
    url = "https://eu-central-1.aws.data.mongodb-api.com/app/data-chnovxv/endpoint/data/v1/action/insertOne"
    headers = { "api-key": "3cyG3EitUZwi6HcI3o8hSS1uIyfHWSe6O58B2kzlmMl9yeMeZFuzERZgwCqwGKjm" }

    documentToAdd = {"device": "MyPico", "readings": [77, 80, 40, 60, 70, 80, 10]}

    insertPayload = {
        "dataSource": "Cluster0",
        "database": "WeatherData2",
        "collection": "BME2802",
        "document": documentToAdd,
    }

    print("sending...")

    response = requests.post(url, headers=headers, json=insertPayload)

    print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))

    if response.status_code == 201:
        print("Added Successfully")
    else:
        print("Error")

    # Always close response objects so we don't leak memory
    response.close()

except Exception as e:
    print(e)

