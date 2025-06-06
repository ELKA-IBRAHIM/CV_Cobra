#import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(24, GPIO.OUT)
#GPIO.output(24, GPIO.LOW)

from gpiozero import LED

led = LED(24)

led.on()