'''
Testet das OLED
'''
from machine import Pin
from time import sleep
from machine import Pin, PWM, ADC,I2C
from ssd1306 import SSD1306_I2C

LED    = machine.Pin("LED",machine.Pin.OUT)                       # use GP25 as an ouput for the Onboard LED
mosfet = Pin(15, Pin.OUT)# SSD1306-Display initialisieren
#----------------------------------------------------------------
#oled
sda_pin = machine.Pin(0)  # Pin 0 für Daten (SDA)
scl_pin = machine.Pin(1)  # Pin 1 für Takt (SCL)
#i2c = machine.I2C(0, sda=sda_pin, scl=scl_pin, freq=400000)
#oled = SSD1306_I2C(128, 64, i2c)
i2c = I2C(0, sda=sda_pin, scl=scl_pin, freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)

oled.text("Hallo", 0, 0)
oled.show()
#-----------------------------------------------
while True:
    LED.value(1)
    mosfet.value(1)
    sleep(0.2)
    LED.value(0)
    mosfet.value(0)
    sleep(2)
            # Take a brief nap to mimic work being done
   
        
    





