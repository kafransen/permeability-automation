#main code for pico to be used to take instructions

#remote control from host via Serial link
#import the packages needed for the various functions
import machine
import sdcard
import uos
from machine import Pin, Timer, WDT
from hx711 import HX711
import utime
import sys
import select

import micropython
micropython.alloc_emergency_exception_buf(100)


#indicate that we are running
led=Pin(28, Pin.OUT)
led.value(1)
utime.sleep(0.5)
led.value(0)


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

# import the information you need
#print('SD card mounted')

from parameters import *


freq=frequency
#set up the scales
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
# print('scales defined')
# def startup():
#     #indicate scales should be placed
#     led=Pin(28, Pin.OUT)
#     #turn on the led
#     led.value(1)
#     #give 5 minutes to set scales up #300 for 5 min
#     utime.sleep(60)
#     #indicate code will run
#     led.value(0)
#     #start writing an sd card file as backup
#     with open("/sd/"+filename+".csv", "w") as file:
#         file.write('time 1,'+scale1+', time 2,'+scale2+','\
#     +'time 3,' +scale3+', time 4,'+ scale4 +','\
#     +'time 5 ,' +scale5+', time 6,'+ scale6+','\
#     +'time 7,'+ scale7+', time 8,'+ scale8+',' \
#     +'time 9 ,'+ scale9+', time 10,' +scale10+','\
#     +'time 11,'+ scale11+', time 12,'+ scale12+','\
#     +'time 13 ,'+ scale13+', time 14,'+ scale14+','\
#     +'time 15,'+ scale15+', time 16,'+ scale16 \
#     +'\n')
# 
#     with open("/sd/"+rtcfilename+".txt","w") as file:
#         file.write('storing rtc for each data point. Rows are list of 16 times, corresponding to scales in order\n')
# 

###decide if data collection should be continued or if it is a continuation
feednum=0

def get_zero(scales):
    #function takes in list of scale hx711 objects
    #function outputs zeros of the scale objects
    zeros=[]
    for scale in scales:
        zero=scale.read_average(30)
        zeros+=[zero]
        #pause between scale readings
        utime.sleep(1)
    return zeros

def start():
    led.value(1)
    utime.sleep(1)
    led.value(0)
    #start watchdog).
    wdt=WDT(timeout=8000) #8 second timeout
    #pull the frequency from outside the function
    global freq, feednum
    minutes=freq
    set_period=minutes*60*1000
    timer=machine.Timer()
    timer.init(mode=Timer.PERIODIC, period=set_period, callback=data_point)
    while feednum<30:
        utime.sleep(5)
        wdt.feed()
        feednum=feednum+1
        print("feednum"+str(feednum))

def data_point(timer):
    #first, feed the watchdog
    wdt=WDT(timeout=8000)
    wdt.feed()
    #feednum=0
    #function takes in list of scale hx711 objects and their zero values
    #function records 16 corresponding measurement times and values
    global freq, feednum,Test #probably isn't needed?
    feednum=0
    rtc=machine.RTC()
    #alternating list of times and values
    timesandvalues=[]
    times=[]
#     print('in function')
    #Done=True
    for i in range(len(scales_list)):
        #print('in loop')
        wdt.feed()
        led.value(1)
        utime.sleep(0.1)
        led.value(0)
        scale=scales_list[i]
        #zero=zero_list[i]
        #initial_i=initial[i]
        #records real displaced time
        times+=[str(rtc.datetime())]
        timesandvalues+=[Test*freq]
        value=scale.read_average(30)
        timesandvalues+=[value]
        utime.sleep_ms(500)
    Test=Test+1
    #print('updating test')
    
    with open("/sd/"+filename+".csv", "a") as file:
        file.write(str(timesandvalues)[1:len(str(timesandvalues))-1]+'\n')
    with open("/sd/"+rtcfilename+".txt","a") as file:
        file.write(str(times)+'\n')
    print(timesandvalues)# this sends info back to the computer
    wdt.feed()
    feednum=0
    if Test>duration:
        stop()
def get_freq():
    print(freq)
def get_duration():
    print(duration)
def get_filename():
    print(filename)
def get_rtcfilename():
    print(rtcfilename)
def get_scalename(Number):
    print(Number)
#set up the timer to handle the periodic data collection
#timer=machine.Timer()   

def stop():
    timer.deinit()
    with open("/sd/stopped.txt","w") as file:
        file.write("test stopped\n")

    
# ##### this is the infinite loop section for looking for serial instructions
###indicate that the pico is now looking for poll instructions

def function_select(message: str):
    if message=='data_point()':
        data_point()
    elif message[4:]=='get_freq':
        get_freq()
    elif message[4:] == 'get_duration':
        get_duration()
    elif message[4:] == 'get_filename':
        get_filename()
    elif message[4:]== 'get_rtcfilename':
        get_rtcfilename()
    elif message[4:]== 'get_scalename(Number)':
        get_scalename(message[14:20])
    elif message=='start()':
        start()
    elif message=='stop()':
        stop()


try:
    file=open("/sd/"+rtcfilename+".txt","r")
    file.close()
    #if you pass the file being present, get the number of rows in text file
    Test= sum(1 for _ in open("/sd/"+rtcfilename+".txt"))
    try:
        file=open("/sd/stopped.txt","r")
        file.close()
    except OSError:
        with open("/sd/timeout.txt", "a") as file:
            file.write("restart after"+ str(Test)+"\n")
        #start the data collection again (this also starts watchdog)
        print("restart")
        start()
except OSError:
    print('no collection started')
    Test=0


#From trying to get individual instructions from computer (timing issues)
# ##### this is the infinite loop section for looking for serial instructions
# poll_obj= select.poll()
# poll.obj.register(sys.stdin, select.POLLIN)
# while True:
#     poll_results=poll_obj.poll(10)
#     if poll_results:
#         message_ = sys.stdin.readline().strip()
#         function_select(message_)



