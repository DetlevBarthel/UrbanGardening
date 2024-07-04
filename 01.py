
#Onboard-LED blinken lassen 
from machine import Pin
from time import sleep

LED    = machine.Pin("LED",machine.Pin.OUT)                       # use GP25 as an ouput for the Onboard LED
counter = 0


while True:
    LED.value(1)
    sleep(2)
    LED.value(0)
    sleep(2)
    counter += 1
    print(counter)