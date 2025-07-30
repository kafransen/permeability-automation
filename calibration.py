#calibration script

import machine
import sdcard
import uos
from machine import Pin, Timer, WDT
from hx711 import HX711
import utime
import sys
import select

#Set up sd card mounting system
CS = machine.Pin(9, machine.Pin.OUT)
spi = machine.SPI(1,baudrate=1000000,polarity=0,phase=0,bits=8,firstbit=machine.SPI.MSB,sck=machine.Pin(10),mosi=machine.Pin(11),miso=machine.Pin(8))
# 
sd = sdcard.SDCard(spi,CS)
# 
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")
# 
sys.path.append("/sd")

from parameters import *

freq=frequency
#define the clock line- shared between all scales

pin_SCK = Pin(0, Pin.OUT)
#Pin numbers are pico GPIO
#Define datapins for each scale
#define each scale

#scale 1
pin_OUT1 = Pin(1, Pin.IN, pull=Pin.PULL_DOWN)
scale_1=HX711(pin_SCK, pin_OUT1)

#scale 2
pin_OUT2 = Pin(2, Pin.IN, pull=Pin.PULL_DOWN)
scale_2=HX711(pin_SCK, pin_OUT2)

#scale 3
pin_OUT3 = Pin(3, Pin.IN, pull=Pin.PULL_DOWN)
scale_3=HX711(pin_SCK, pin_OUT3)

#scale 4
pin_OUT4 = Pin(4, Pin.IN, pull=Pin.PULL_DOWN)
scale_4=HX711(pin_SCK, pin_OUT4)

#scale 5
pin_OUT5 = Pin(5, Pin.IN, pull=Pin.PULL_DOWN)
scale_5=HX711(pin_SCK, pin_OUT5)

#scale 6
pin_OUT6 = Pin(6, Pin.IN, pull=Pin.PULL_DOWN)
scale_6=HX711(pin_SCK, pin_OUT6)

#scale 7
pin_OUT7 = Pin(7, Pin.IN, pull=Pin.PULL_DOWN)
scale_7=HX711(pin_SCK, pin_OUT7)

#scale 8, Pin 12
pin_OUT8 = Pin(12, Pin.IN, pull=Pin.PULL_DOWN)
scale_8=HX711(pin_SCK, pin_OUT8)

#scale 9, Pin 13
pin_OUT9 = Pin(13, Pin.IN, pull=Pin.PULL_DOWN)
scale_9=HX711(pin_SCK, pin_OUT9)

#scale 10, pin 14
pin_OUT10 = Pin(14, Pin.IN, pull=Pin.PULL_DOWN)
scale_10=HX711(pin_SCK, pin_OUT10)

#scale 11, pin 15
pin_OUT11 = Pin(15, Pin.IN, pull=Pin.PULL_DOWN)
scale_11=HX711(pin_SCK, pin_OUT11)

#scale 12, pin 16
pin_OUT12 = Pin(16, Pin.IN, pull=Pin.PULL_DOWN)
scale_12=HX711(pin_SCK, pin_OUT12)

#scale 13, pin 17
pin_OUT13 = Pin(17, Pin.IN, pull=Pin.PULL_DOWN)
scale_13=HX711(pin_SCK, pin_OUT13)

#scale 14, pin 18
pin_OUT14 = Pin(18, Pin.IN, pull=Pin.PULL_DOWN)
scale_14=HX711(pin_SCK, pin_OUT14)

#scale 15, pin 19
pin_OUT15 = Pin(19, Pin.IN, pull=Pin.PULL_DOWN)
scale_15=HX711(pin_SCK, pin_OUT15)

#scale 16, pin 20
pin_OUT16 = Pin(20, Pin.IN, pull=Pin.PULL_DOWN)
scale_16=HX711(pin_SCK, pin_OUT16)

scales_list=[scale_1, scale_2, scale_3, scale_4, scale_5, scale_6, scale_7, scale_8, scale_9, scale_10, scale_11, scale_12, scale_13, scale_14, scale_15, scale_16]


def calibrate(list_scales):
    print("Calibrate the scales")
    masses=[85,90,92,93,95,100]
    with open("/sd/"+filename+"_calibration.csv", "w") as file:
            file.write('Scale,85,90,92,93,95,100\n')
    for i in range(16):
        scale=list_scales[i]
#         scale.tare() #decided not to tare because you don't have taring when everything resets
        values=[]
        for j in masses:
            print('scale ', str(i+1) ,"mass ", j)
            led=Pin(28,Pin.OUT)
            led.value(1)
            utime.sleep(10) #allow 10 seconds for weight placement
            led.value(0)
            reading=scale.read_average()
            values+=[reading]
        with open("/sd/"+filename+"_calibration.csv", "a") as file:
            file.write('Scale '+str(i+1)+','+str(values[0])+','+str(values[1])+','+str(values[2])+','+str(values[3])+','\
                       + str(values[4])+','+str(values[5])
                       +'\n')
        print('finished scale'+str(i+1))
        
if __name__=='__main__':
    calibrate(scales_list)
    print('calibration_finished')
    