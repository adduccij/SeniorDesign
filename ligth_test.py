
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)
 
for i in range(0,1000):
    print GPIO.input(4)
    time.sleep(2)
