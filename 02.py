'''
Schaltet eine externe LED
'''

from machine import WDT   #Watch Dog Timer class
from machine import Pin
from time import sleep

LED    = machine.Pin("LED",machine.Pin.OUT)                       # use GP25 as an ouput for the Onboard LED

led_extern = Pin(15, Pin.OUT)

while True:
    LED.value(1)
    led_extern.value(1)
    sleep(1)
    LED.value(0)
    led_extern.value(0)
    sleep(1)
            # Take a brief nap to mimic work being done
   
        
    





